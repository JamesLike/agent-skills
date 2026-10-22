# Advanced Repository and PR Management

## Fork Synchronization
```bash
gh repo sync                                  # sync local fork from upstream
gh repo sync --branch v1                      # sync specific branch
gh repo sync owner/fork                       # sync remote fork from parent
gh repo sync owner/repo --source owner2/repo2 # custom source repo
gh repo sync --force                          # hard reset when diverged
```
- Tries fast-forward first; use `--force` only for diverged branches
- Validates for uncommitted changes before syncing current branch

## PR Merge Strategies
```bash
gh pr merge --merge                    # merge commit
gh pr merge --squash                   # squash and merge
gh pr merge --rebase                   # rebase and merge
gh pr merge --auto                     # enable auto-merge (waits for required checks)
gh pr merge --disable-auto             # disable auto-merge
gh pr merge --admin                    # bypass protections and merge queue
gh pr merge --match-head-commit <sha>  # safety: verify HEAD before merging
gh pr merge -d                         # delete branch after merge
gh pr merge --subject "Custom msg"     # custom merge commit subject
gh pr merge --body "Details"           # custom merge commit body
gh pr merge --body-file CHANGELOG.md   # body from file
gh pr merge --author-email a@b.com     # custom author email
```
- For repos with merge queue: merge enqueues automatically (no strategy flag needed)
- `--admin` bypasses both branch protections and merge queue

## PR Checks
```bash
gh pr checks                           # show CI status for current branch
gh pr checks --watch                   # poll until all complete
gh pr checks --watch --fail-fast       # stop on first failure
gh pr checks --required                # only required checks
gh pr checks --json name,state,bucket  # structured output
```
- Exit code 8 = checks still pending
- `bucket` values: pass, fail, pending, skipping, cancel

## PR Edit
```bash
gh pr edit --title "New title"
gh pr edit --body "New description"
gh pr edit --body-file desc.md
gh pr edit --base main                 # change base branch
gh pr edit --add-reviewer user1,org/team
gh pr edit --remove-reviewer user1
gh pr edit --add-assignee @me          # assign yourself
gh pr edit --add-assignee @copilot     # GitHub AI reviewer
gh pr edit --add-label bug,urgent
gh pr edit --remove-label wontfix
gh pr edit --add-project "Project Name"
gh pr edit --milestone "v1.0"
gh pr edit --remove-milestone
```

## PR Draft Management
```bash
gh pr ready                            # mark draft as ready for review
gh pr ready --undo                     # convert back to draft
```

## PR Review
```bash
gh pr review --approve
gh pr review --request-changes --body "Please fix X"
gh pr review --comment --body "Looks good overall"
gh pr review --body-file review.md
```

## PR Diff
```bash
gh pr diff                             # unified diff
gh pr diff --patch                     # patch format
gh pr diff --name-only                 # changed file names only (for scripting)
gh pr diff --color always              # force color
```

## Issue Development Branches
```bash
gh issue develop 123                   # create linked branch
gh issue develop 123 --checkout        # create and switch to it
gh issue develop 123 --base my-feature # branch from specific base
gh issue develop 123 --name custom-branch  # custom branch name
gh issue develop --list 123            # list branches linked to issue
gh issue develop 123 --branch-repo owner/other  # branch in different repo
```

## Issue Operations
```bash
gh issue transfer 123 owner/other-repo # transfer to another repo
gh issue pin 123                        # pin to repo
gh issue unpin 123                      # unpin
gh issue lock 123                       # lock discussion
gh issue list --search "is:open sort:created-asc"  # advanced search syntax
```

## Repository Autolinks
```bash
gh repo autolink create JIRA- "https://jira.example.com/browse/JIRA-<num>"
gh repo autolink list
gh repo autolink view <id>
gh repo autolink delete <id>
```

## Deploy Keys
```bash
gh repo deploy-key add key.pub --title "CI deploy"
gh repo deploy-key list
gh repo deploy-key delete <id>
```

## Projects v2
```bash
gh project list --owner @me
gh project view <number>
gh project create --title "Sprint 1"
gh project item-list <number>
gh project item-add <number> --url <issue-or-pr-url>
gh project item-edit --id <item-id> --field-id <field-id> --text "value"
gh project field-list <number>
gh project field-create <number> --name "Priority" --data-type SINGLE_SELECT
gh project close <number>
gh project delete <number>
gh project link <number> --repo owner/repo
```
Note: Projects v2 requires the `project` scope. Add with: `gh auth refresh -s project`
