# JSON, jq, and Template Output

## Field Discovery
Run any command with `--json` and no field list to see all available fields:
```bash
gh pr list --json          # lists all PR fields
gh issue view 1 --json     # lists all issue fields
```

## PR Fields (--json)
assignees, author, autoMergeRequest, baseRefName, baseRefOid, body, changedFiles, closed, closedAt, closingIssuesReferences, comments, commits, createdAt, deletions, files, fullDatabaseId, headRefName, headRefOid, headRepository, headRepositoryOwner, id, isCrossRepository, isDraft, labels, latestReviews, maintainerCanModify, mergeable, mergeCommit, mergedAt, mergedBy, mergeStateStatus, milestone, number, potentialMergeCommit, projectCards, projectItems, reactionGroups, reviewDecision, reviewRequests, reviews, state, statusCheckRollup, title, updatedAt, url

## Issue Fields (--json)
assignees, author, body, closed, closedAt, closedByPullRequestsReferences, comments, createdAt, id, isPinned, labels, milestone, number, projectCards, projectItems, reactionGroups, state, stateReason, title, updatedAt, url

## Check Fields (gh pr checks --json)
name, state, startedAt, completedAt, link, bucket, event, workflow, description
- `bucket` values: pass, fail, pending, skipping, cancel

## jq Patterns

```bash
# Select single field from list
gh pr list --json title --jq '.[].title'

# Filter items
gh pr list --json title,state --jq '.[] | select(.state == "OPEN")'

# Multiple fields
gh pr list --json number,title,author --jq '.[] | {number, title, author: .author.login}'

# Count
gh pr list --json number --jq 'length'

# Extract nested values
gh pr list --json labels --jq '.[].labels[].name'

# Unique values
gh issue list --json labels --jq '[.[].labels[].name] | unique'

# String interpolation (tab-separated)
gh pr list --json number,title --jq '.[] | "\(.number)\t\(.title)"'

# Complex filtering
gh pr list --json title,labels --jq 'map(select((.labels | length) > 0))'

# Group and count
gh run list --json status --jq 'group_by(.status) | map({status: .[0].status, count: length})'
```

## Go Template Functions

Available with `--template`:

| Function | Signature | Description |
|----------|-----------|-------------|
| `autocolor` | `autocolor <style> <input>` | Colorize only when connected to terminal |
| `color` | `color <style> <input>` | Force colorize (mgutz/ansi styles) |
| `join` | `join <sep> <list>` | Join array with separator |
| `pluck` | `pluck <field> <list>` | Extract field from all items |
| `tablerow` | `tablerow <fields>...` | Align fields as table columns |
| `tablerender` | `tablerender` | Render accumulated tablerow output |
| `timeago` | `timeago <time>` | Relative timestamp ("about 2 hours ago") |
| `timefmt` | `timefmt <format> <time>` | Format with Go time format |
| `truncate` | `truncate <length> <input>` | Truncate string to length |
| `hyperlink` | `hyperlink <url> <text>` | Terminal hyperlink (OSC 8) |

Sprig functions: `contains`, `hasPrefix`, `hasSuffix`, `regexMatch`

Color styles: `green`, `red`, `yellow`, `blue`, `cyan`, `magenta`, `white`, `black`, append `+b` for bold, `+h` for highlight (e.g., `red+b`)

## Template Recipes

```bash
# Simple table
gh pr list --json number,title,author,updatedAt --template \
  '{{range .}}{{tablerow (printf "#%v" .number | autocolor "green") .title .author.login (timeago .updatedAt)}}{{end}}'

# Hyperlinked list
gh issue list --json title,url --template \
  '{{range .}}{{hyperlink .url .title}}{{"\n"}}{{end}}'

# Table with headers
gh pr view 123 --json assignees,reviews --template '
{{tablerow "ASSIGNEE" "NAME"}}{{range .assignees}}{{tablerow .login .name}}{{end}}{{tablerender}}
{{tablerow "REVIEWER" "STATE"}}{{range .reviews}}{{tablerow .author.login .state}}{{end}}{{tablerender}}'

# Colored labels
gh issue list --json number,title,labels --template \
  '{{range .}}{{.title}} ({{.labels | pluck "name" | join ", " | color "yellow"}}){{"\n"}}{{end}}'
```
