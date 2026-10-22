# Scripting Patterns

## TTY Detection and Non-Interactive Mode
- Many commands change behavior (prompts, colors, formatting) based on TTY
- When stdout is NOT a TTY: no colors, full URLs, tab-separated columns, no truncation, no header
- `GH_FORCE_TTY=120` forces terminal-style output with 120-column width
- `GH_PROMPT_DISABLED=1` prevents prompts (fails with error instead of hanging)
- Useful: `GH_FORCE_TTY=1 gh pr list | fzf` to get colored output in fzf

## Exit Code Handling
```bash
# gh pr checks returns 8 when checks are pending
gh pr checks --watch --fail-fast
if [ $? -eq 0 ]; then echo "All checks passed"
elif [ $? -eq 8 ]; then echo "Checks still pending"
else echo "Checks failed"; fi

# gh run watch --exit-status returns 1 on failure
gh run watch $RUN_ID --exit-status && echo "Run succeeded" || echo "Run failed"
```

## Batch Operations
Pattern: `gh <cmd> list --json <fields> --jq '...' | xargs -I{} gh <cmd> ...`

```bash
# Close all stale issues
gh issue list --json number --jq '.[].number' --label stale | \
  xargs -I{} gh issue close {}

# Add label to search results
gh search issues "bug" --repo owner/repo --json number --jq '.[].number' | \
  xargs -I{} gh issue edit {} --add-label "triage"

# Parallel batch (4 concurrent)
gh pr list --json number --jq '.[].number' --state closed | \
  xargs -P 4 -I{} gh pr view {} --json title --jq '.title'

# Delete all draft PRs
gh pr list --draft --json number --jq '.[].number' | \
  xargs -I{} gh pr close {}

# Rerun all failed workflow runs
gh run list --status failure --json databaseId --jq '.[].databaseId' | \
  xargs -I{} gh run rerun {}
```

## Repository Context Override
```bash
# Per-command override
gh pr list -R owner/other-repo

# Session-wide override
export GH_REPO=owner/other-repo
gh pr list    # operates on owner/other-repo

# Loop across repos
for repo in owner/repo1 owner/repo2 owner/repo3; do
  gh issue list -R "$repo" --json number --jq 'length'
done
```

## Authentication Patterns
```bash
# Per-command token override
GH_TOKEN=ghp_xxx gh api /user

# Get current token for use in other tools
TOKEN=$(gh auth token)
curl -H "Authorization: Bearer $TOKEN" https://api.github.com/user

# Check auth state and scopes
gh auth status
gh api -i /user 2>/dev/null | grep X-OAuth-Scopes

# Multiple accounts
gh auth login                        # additive (keeps existing)
gh auth switch                       # switch active account
gh auth token --user username        # get specific user's token
```

## Debugging
```bash
GH_DEBUG=1 gh pr list                # verbose logging to stderr
GH_DEBUG=api gh api /user            # full HTTP request/response bodies
gh api --verbose /user               # same as GH_DEBUG=api per-command
```
