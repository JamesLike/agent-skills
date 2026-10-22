# gh search Advanced Filtering

## Five Search Types

| Command | Searches | Key JSON Fields |
|---------|----------|-----------------|
| `gh search issues` | Issues | assignees, author, body, closedAt, commentsCount, createdAt, id, isLocked, isPullRequest, labels, number, repository, state, title, updatedAt, url |
| `gh search prs` | Pull requests | (same as issues) + isDraft |
| `gh search repos` | Repositories | createdAt, defaultBranch, description, forksCount, fullName, id, isArchived, isFork, isPrivate, language, license, name, openIssuesCount, owner, stargazersCount, updatedAt, url, visibility, watchersCount |
| `gh search code` | Code | path, repository, sha, textMatches, url |
| `gh search commits` | Commits | author, commit, committer, sha, id, parents, repository, url |

## Issue/PR Qualifiers (shared)

List all: --assignee, --author, --app, --closed, --commenter, --comments, --created, --interactions, --involves, --label (multiple allowed), --language, --locked, --match {title|body|comments}, --mentions, --milestone, --no-assignee, --no-label, --no-milestone, --no-project, --owner (multiple), --project, --reactions, --repo/-R (multiple), --state {open|closed}, --team-mentions, --updated, --visibility {public|private|internal}, --archived

## PR-Only Qualifiers

--base/-B, --head/-H, --draft, --merged, --merged-at, --review {none|required|approved|changes_requested}, --review-requested, --reviewed-by, --checks {pending|success|failure}

## Repository Qualifiers

--archived, --created, --followers, --forks, --good-first-issues, --help-wanted-issues, --include-forks {false|true|only}, --language, --license, --match {name|description|readme}, --number-topics, --owner, --size (kb), --stars, --topic (multiple), --updated, --visibility

## Code Qualifiers

--extension, --filename, --language, --match {file|path}, --owner, --repo, --size

## Commit Qualifiers

--author, --author-date, --author-email, --author-name, --committer, --committer-date, --committer-email, --committer-name, --hash, --merge, --owner, --parent, --repo, --tree, --visibility

## Sort Options

- Issues/PRs: --sort {best-match|comments|created|interactions|reactions|reactions-+1|reactions--1|reactions-heart|reactions-smile|reactions-tada|reactions-thinking_face|updated}
- Repos: --sort {best-match|forks|help-wanted-issues|stars|updated}
- Commits: --sort {best-match|author-date|committer-date}
- All: --order {asc|desc}

## Range and Exclusion Syntax

- Ranges: `--comments ">100"`, `--stars "10..50"`, `--created ">=2024-01-01"`
- Exclusion: use `--` separator: `gh search issues -- "query -label:bug"`
- Max 1000 results (`--limit` max)
- Common: --limit/-L (default 30), --json, --jq, --template, --web/-w
