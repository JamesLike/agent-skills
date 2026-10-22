# CI/CD Automation with gh

## Workflow Dispatch

```bash
# Trigger by name/ID/filename
gh workflow run <workflow> [-f key=value...] [-F key=@file] [--ref branch]

# JSON input from stdin
echo '{"name":"value"}' | gh workflow run triage.yml --json

# Interactive (prompts for workflow + inputs from workflow_dispatch config)
gh workflow run
```

- `-f`: raw string values, `-F`: typed values (same rules as `gh api`)
- `--ref`: target branch (default: repo default branch)
- Workflow must have `on: workflow_dispatch` trigger

## Workflow Management

```bash
gh workflow list                    # list with status
gh workflow view <workflow>         # view details
gh workflow enable <workflow>       # enable disabled workflow
gh workflow disable <workflow>      # disable workflow
```

## Run Monitoring

```bash
gh run list [--workflow=name] [--branch=b] [--user=u] [--status=s] [--event=e] [--created="date"]
gh run view <id>                    # detailed status
gh run view <id> --log              # full logs
gh run view <id> --log-failed       # only failed step logs
gh run watch <id>                   # poll until completion
gh run watch <id> --exit-status     # exit non-zero on failure (for scripts)
gh run watch <id> --compact         # show only relevant/failed steps
gh run watch <id> --interval 5      # custom polling (seconds)
gh run cancel <id>
gh run rerun <id>                   # rerun all jobs
gh run rerun <id> --failed          # rerun only failed jobs
gh run delete <id>
```

- `--exit-status` exits 1 on failure (essential for CI scripts)
- Status values: queued, in_progress, completed, requested, waiting, action_required, cancelled, failure, neutral, skipped, stale, startup_failure, success, timed_out

## Artifacts

```bash
gh run download <run-id>                        # all artifacts
gh run download <run-id> -n <artifact-name>     # specific artifact
gh run download <run-id> -D <directory>          # custom output dir
gh run download <run-id> -p <glob-pattern>       # pattern match
```

## Release Management

```bash
gh release create <tag> [files...]               # create with assets
gh release create <tag> --generate-notes         # auto-generate notes from commits
gh release create <tag> --notes-start-tag <tag>  # set start for auto-notes
gh release create <tag> -F notes.md              # notes from file
gh release create <tag> --draft                  # draft release
gh release create <tag> --prerelease             # prerelease
gh release create <tag> --latest=false           # don't mark as latest
gh release create <tag> --target <branch>        # target branch
gh release create <tag> --discussion-category "Announcements"
gh release create <tag> './dist/*.tgz'           # glob for assets
gh release create <tag> 'app.zip#My Display Label'  # asset with label

gh release upload <tag> <files...>               # add assets to existing
gh release download <tag> [-p "*.tar.gz"]        # download assets
gh release edit <tag> [--draft=false] [--prerelease=false]
gh release delete <tag> [--yes] [--cleanup-tag]
gh release delete-asset <tag> <asset-name>
gh release list [--limit N]
gh release view <tag> [--web]
```

## Cache Management

```bash
gh cache list [--limit N] [--json]
gh cache delete <cache-id-or-key>
gh cache delete --all
```

## Attestation Verification

```bash
gh attestation verify <artifact> -o <owner>      # verify SLSA provenance
gh attestation download <artifact-uri>            # download attestation bundle
gh attestation inspect <bundle>                   # view details
```
