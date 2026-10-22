# gh api Advanced Usage

## REST API Patterns

- Path placeholders: `{owner}`, `{repo}`, `{branch}` auto-fill from current repo context (or `GH_REPO` env var).
- Method detection: auto-POSTs when fields are provided; use `-X GET` to override.
- Custom headers: `-H 'Accept: application/vnd.github.v3.raw+json'`.
- API previews: `--preview baptiste,nebula` (auto-generates the Accept header).
- Caching: `--cache 3600s` (accepts Go durations: `60m`, `1h`).
- Include response headers: `-i` / `--include`.
- Show full request/response: `--verbose`.
- Suppress output: `--silent`.

```bash
# GET with placeholder expansion
gh api repos/{owner}/{repo}/branches/{branch}

# Force GET even when fields are present
gh api repos/{owner}/{repo}/issues -X GET -F per_page=5

# Cache the response for one hour
gh api repos/{owner}/{repo}/releases --cache 1h

# Inspect raw request and response
gh api repos/{owner}/{repo} --verbose
```

## Field Types: `-F` vs `-f`

Use `-f` (--raw-field) when the value must remain a literal string.
Use `-F` (--field) when automatic type conversion is desired.

| Flag | Behavior |
|------|----------|
| `-f key=value` | Value is always a raw string. |
| `-F key=true` | Converts to JSON boolean `true`. |
| `-F key=false` | Converts to JSON boolean `false`. |
| `-F key=null` | Converts to JSON `null`. |
| `-F key=42` | Converts to JSON number `42`. |
| `-F key=@filename` | Reads file contents as the value. |
| `-F key=@-` | Reads from stdin. |
| `-F key={owner}` | Placeholder expansion. |

For GraphQL requests, all fields except `query` and `operationName` become query variables automatically.

## Nested and Complex Parameters

Build nested JSON objects and arrays directly from the command line.

```bash
# Nested object
gh api repos/{owner}/{repo}/hooks \
  -f name=web \
  -F active=true \
  -F 'config[url]=https://example.com/webhook' \
  -F 'config[content_type]=json' \
  -F 'config[secret]=mysecret'

# Array values
gh api repos/{owner}/{repo}/hooks \
  -F 'events[]=push' \
  -F 'events[]=pull_request'

# Empty array
gh api repos/{owner}/{repo}/hooks \
  -F 'events[]='

# Deeply nested structures
gh api repos/{owner}/{repo}/rulesets \
  -f name=my-ruleset \
  -f target=branch \
  -f enforcement=active \
  -F 'properties[][property_name]=env' \
  -F 'properties[][allowed_values][]=staging' \
  -F 'properties[][allowed_values][]=production'
```

## File and Stdin Input

Supply request bodies from files or stdin instead of inline fields.

```bash
# Single field from a file
gh api repos/{owner}/{repo}/issues -f title="From file" -F body=@README.md

# Single field from stdin
echo "Piped body text" | gh api repos/{owner}/{repo}/issues -f title="Stdin" -F body=@-

# Entire JSON body from a file
gh api repos/{owner}/{repo}/issues --input issue.json

# Entire JSON body from stdin
cat payload.json | gh api repos/{owner}/{repo}/dispatches --input -
```

When using `--input`, any `-f`/`-F` parameters are appended to the query string rather than the request body.

## GraphQL Queries

Send GraphQL requests by providing a `query` field.

```bash
# Basic query
gh api graphql -f query='query { viewer { login } }'

# Query with variables (placeholder + type conversion)
gh api graphql \
  -f query='
    query($owner: String!, $name: String!, $count: Int!) {
      repository(owner: $owner, name: $name) {
        issues(first: $count, states: OPEN) {
          nodes { title number }
        }
      }
    }
  ' \
  -F owner='{owner}' \
  -F name='{repo}' \
  -F count=10
```

- `-F count=10` auto-converts to integer because of `-F` magic.
- `-F owner='{owner}'` expands the `{owner}` placeholder.

## GraphQL Pagination

Paginate through all pages of a GraphQL connection automatically.

```bash
gh api graphql --paginate -f query='
  query($endCursor: String) {
    viewer {
      repositories(first: 100, after: $endCursor) {
        nodes { nameWithOwner }
        pageInfo { hasNextPage endCursor }
      }
    }
  }
'
```

Requirements for `--paginate` with GraphQL:

1. Declare `$endCursor: String` as a query variable (do not provide a value).
2. Pass `after: $endCursor` to the paginated connection.
3. Request `pageInfo { hasNextPage endCursor }` in the response.

Collect all pages into a single JSON array with `--slurp`:

```bash
gh api graphql --paginate --slurp -f query='...'
```

**Limitation:** `--slurp` cannot be combined with `--jq` or `--template`. Pipe to an external `jq` instead:

```bash
gh api graphql --paginate --slurp -f query='...' | jq '.[].data.viewer.repositories.nodes[].nameWithOwner'
```

## Response Filtering

### jq Expressions

Filter JSON responses inline with `--jq`.

```bash
# Extract issue titles
gh api repos/{owner}/{repo}/issues --jq '.[].title'

# Select specific fields
gh api repos/{owner}/{repo}/pulls --jq '.[] | {number, title, user: .user.login}'

# Filter with conditions
gh api repos/{owner}/{repo}/issues --jq '[.[] | select(.labels[].name == "bug")] | length'
```

### Go Templates

Format output with Go templates via `--template`.

```bash
gh api repos/{owner}/{repo}/issues --template '{{range .}}{{.title}} (#{{.number}}){{"\n"}}{{end}}'

gh api repos/{owner}/{repo}/releases --template '{{range .}}{{.tag_name}}{{"\t"}}{{.name}}{{"\n"}}{{end}}'
```

## Common Patterns

### List all releases (paginated)

```bash
gh api repos/{owner}/{repo}/releases --paginate --jq '.[].tag_name'
```

### Create an issue with labels

```bash
gh api repos/{owner}/{repo}/issues \
  -f title="Bug: login broken" \
  -f body="Steps to reproduce..." \
  -F 'labels[]=bug' \
  -F 'labels[]=priority:high'
```

### Get raw file content

```bash
gh api repos/{owner}/{repo}/contents/README.md \
  -H "Accept: application/vnd.github.v3.raw"
```

### Look up authenticated user via GraphQL

```bash
gh api graphql -f query='
  query {
    viewer {
      login
      name
      email
      repositories(first: 5, orderBy: {field: UPDATED_AT, direction: DESC}) {
        nodes { nameWithOwner stargazerCount }
      }
    }
  }
'
```

### Add a comment to a PR

```bash
gh api repos/{owner}/{repo}/issues/42/comments -f body="Looks good to merge."
```

### Trigger a workflow dispatch

```bash
gh api repos/{owner}/{repo}/actions/workflows/ci.yml/dispatches \
  -F ref=main \
  -F 'inputs[environment]=staging'
```

### Delete a release by tag

```bash
RELEASE_ID=$(gh api repos/{owner}/{repo}/releases/tags/v1.0.0 --jq '.id')
gh api -X DELETE repos/{owner}/{repo}/releases/$RELEASE_ID
```
