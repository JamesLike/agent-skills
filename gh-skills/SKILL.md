---
name: gh-skills
description: "Power-user guide for the GitHub CLI (gh). Use when working with: gh api (GraphQL queries, REST pagination, field types, nested parameters), gh search (issue/PR/repo/code/commit qualifiers), CI/CD automation (workflow dispatch, run watching, release creation), JSON/jq/template output formatting across commands, scripting patterns (TTY detection, exit codes, batch operations with xargs), or advanced repository and PR management (merge strategies, auto-merge, fork sync, issue develop branches, Projects v2). Trigger on questions about gh CLI automation, scripting, advanced flags, or non-obvious features."
---

# GitHub CLI Power User Guide

## Core Principles

- Prefer `gh` subcommands over raw `gh api` when a subcommand exists
- Use `--json <fields> --jq <expr>` for machine-readable output (never parse human-formatted tables)
- Discover available JSON fields: run any command with `--json` and no field list
- Use `-F` (typed/magic) for JSON types, file reads, and placeholders; use `-f` for raw strings

## Reference Navigation

Load the appropriate reference file based on the task:

| Task | Reference |
|------|-----------|
| Call GitHub REST/GraphQL API directly | [references/api-advanced.md](references/api-advanced.md) |
| Search issues, PRs, repos, code, or commits | [references/search-and-filtering.md](references/search-and-filtering.md) |
| Trigger workflows, watch runs, create releases, manage caches | [references/cicd-automation.md](references/cicd-automation.md) |
| Format output with `--json`, `--jq`, or `--template` | [references/json-templates-jq.md](references/json-templates-jq.md) |
| Write non-interactive scripts, batch operations | [references/scripting-patterns.md](references/scripting-patterns.md) |
| Advanced PR merging, fork sync, issue branches, Projects v2 | [references/repo-pr-management.md](references/repo-pr-management.md) |

## Critical Gotchas

### `-F` vs `-f` for `gh api`

```bash
# -f: value is ALWAYS a raw string
gh api repos/{owner}/{repo}/issues -f title="Bug report" -f body="Details"

# -F: magic conversion -- true/false/null -> JSON types, integers -> numbers,
#     @file -> file contents, {owner}/{repo}/{branch} -> repo context
gh api repos/{owner}/{repo}/issues -F draft=true -F milestone=3 -F body=@body.md
```

For GraphQL: all `-F`/`-f` fields except `query` and `operationName` become GraphQL variables.

### Pagination constraints

- **REST**: works only with GET requests; auto-adds `per_page=100`
- **GraphQL**: query MUST accept `$endCursor: String` and return `pageInfo { hasNextPage endCursor }`
- `--slurp` wraps all pages into one JSON array (requires `--paginate`; cannot combine with `--jq`/`--template` -- pipe to external `jq` instead)

### Nested parameter syntax

```bash
# Nested objects
gh api endpoint -F 'config[url]=https://example.com' -F 'config[secret]=mysecret'

# Arrays
gh api endpoint -F 'events[]=push' -F 'events[]=pull_request'

# Empty array
gh api endpoint -F 'events[]='
```

### Exit codes

| Code | Meaning |
|------|---------|
| 0 | Success |
| 1 | Error |
| 2 | Cancelled |
| 4 | Authentication required |
| 8 | Checks pending (`gh pr checks`) |

### TTY detection

- Commands auto-detect TTY: add colors, truncate, prompt when interactive
- `GH_FORCE_TTY=<width>` forces terminal-style output in pipes (e.g., `GH_FORCE_TTY=120`)
- `GH_PROMPT_DISABLED=1` prevents all interactive prompts

## Environment Variables

| Variable | Purpose |
|----------|---------|
| `GH_TOKEN` / `GITHUB_TOKEN` | Auth token for github.com |
| `GH_ENTERPRISE_TOKEN` | Auth token for GHES |
| `GH_HOST` | Default GitHub hostname |
| `GH_REPO` | Override repository as `[HOST/]OWNER/REPO` |
| `GH_EDITOR` | Text editor (fallback: `GIT_EDITOR`, `VISUAL`, `EDITOR`) |
| `GH_BROWSER` | Web browser (fallback: `BROWSER`) |
| `GH_PAGER` | Pager program (fallback: `PAGER`) |
| `GH_DEBUG` | `1` for verbose, `api` for HTTP request/response bodies |
| `GH_FORCE_TTY` | Force TTY output (number=columns, percent=viewport%) |
| `GH_PROMPT_DISABLED` | Disable interactive prompts |
| `NO_COLOR` | Disable ANSI colors |
| `CLICOLOR_FORCE` | Force colors in piped output (non-zero) |
| `GH_CONFIG_DIR` | Override config directory |
| `GH_NO_UPDATE_NOTIFIER` | Suppress version check |

## Configuration

```bash
gh config set git_protocol ssh       # {https|ssh}
gh config set editor vim             # text editor
gh config set prompt enabled         # {enabled|disabled}
gh config set pager less             # pager program
gh config set browser firefox        # web browser
gh config set git_protocol ssh --host github.example.com  # per-host
gh config list                       # show all
gh config clear-cache                # clear HTTP cache
```

## Aliases

```bash
# Simple shortcut
gh alias set pv 'pr view'

# Positional arguments ($1, $2, ...)
gh alias set epicsBy 'issue list --author="$1" --label="epic"'

# Shell expression (pipes, redirection)
gh alias set --shell igrep 'gh issue list --label="$1" | grep "$2"'
# Or with ! prefix
gh alias set igrep '!gh issue list --label="$1" | grep "$2"'

# Overwrite existing
gh alias set --clobber pv 'pr view --web'

# From stdin
echo 'pr list --state merged' | gh alias set merged -

# Manage
gh alias list
gh alias delete pv
gh alias import aliases.yml
```

## Extension Ecosystem

```bash
gh extension search <query>                      # find extensions
gh extension install owner/gh-extension          # install
gh extension install . --pin v1.0.0              # local dev / pinned version
gh extension list                                # show installed
gh extension upgrade --all                       # update all
gh extension upgrade <name> --dry-run            # preview update
gh extension browse                              # interactive browser (TTY)
gh extension create <name>                       # scaffold new extension
gh extension create foobar --precompiled=go      # Go extension
gh extension exec <name> [args]                  # run when name conflicts
gh extension remove <name>                       # uninstall
```
