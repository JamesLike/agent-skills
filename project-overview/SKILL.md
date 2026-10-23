---
name: project-overview
description: Set up or refresh a project's shared agent context in the central research-hub repo (~/projects/research-hub), so any agent (Claude Code, OpenCode, etc.) on any machine (mac, S3DF/psana, other clusters) can pick up the work. Creates projects/<name>/ in the hub (CARD, STATUS, TODO, DECISIONS, methods, locations, handoffs), registers the project in PROJECTS.md and repos.conf, distills grants/talks/papers into project and shared science context, and gives the code repo a short AGENTS.md/CLAUDE.md pointing to the hub. Trigger on requests like "write a project overview", "set up AGENTS.md", "add this project to the hub", "make this repo agent-ready", "scaffold project context", "distill my grant into project context", "set up handoffs", or "refresh the project overview".
---

# Project Overview → research-hub

All agent context, progress, and handoffs live in one central repo, **research-hub**, cloned at
`~/projects/research-hub` on every machine (GitHub: `JamesLike/research-hub`). Code repos and
cluster folders hold code, analysis, and data, and the hub records **where** they are.

```
~/projects/research-hub/
├── AGENTS.md  machines.md  PROJECTS.md  repos.conf  sync.sh  prompts/{start,end}.md
├── science/  grants/  literature/  talks/        # shared across projects
└── projects/
    ├── _template/                               # canonical templates: copy, don't reinvent
    └── <name>/  CARD.md STATUS.md TODO.md DECISIONS.md methods.md locations.md handoffs/
```

Principles:
1. **The hub is the only shared memory.** Nothing important lives only in `~/.claude`, OpenCode
   sessions, chat history, or uncommitted files.
2. **Pointers, not copies.** Never copy code or data into the hub. Record path + machine +
   repo@commit in `locations.md`.
3. **Distill, don't dump.** Short, sourced summaries; originals go in `originals/` (git-ignored).
4. **Never invent science.** Tag claims `[src: <file> §<section>]`, or mark them `TODO(verify)`.
5. **Never overwrite silently.** Merge into existing files and show the diff.
6. **Handoffs are append-only.** One new file per session; earlier ones are never edited.

## 0. Locate the hub

- `HUB=~/projects/research-hub`. If it's missing, ask: clone it
  (`git clone git@github.com:JamesLike/research-hub.git ~/projects/research-hub`), or, if the user
  has no hub, use standalone mode (see the end of this file).
- Run `$HUB/sync.sh` to get the latest hub. Read `$HUB/AGENTS.md` and `$HUB/machines.md`, and
  identify the current machine.
- The project `<name>` defaults to the code repo's folder name. Confirm it if ambiguous.

## 1. Survey

Do this before asking the user anything.

- **Hub:** does `projects/<name>/` exist? If so, this is a **refresh** (see below). Also check
  `PROJECTS.md`, `repos.conf`, and any `grants/` or `science/` content relevant to this project.
- **Code repo** (if there is one): layout (`git ls-files | head -200`), README, build/test config
  (`pyproject.toml`, `environment.yml`, `Makefile`, CI), SLURM scripts, existing `AGENTS.md`,
  `CLAUDE.md`, `docs/`, `TODO*`, and `git log --oneline -30`. Note the remote URL, branch, and HEAD SHA.
- **Locations:** look for hard-coded paths (`/sdf/...`, scratch dirs, data dirs), `sbatch` headers,
  experiment/run IDs, and output directories. These seed `locations.md`.
- **Project without a repo** (e.g. analysis folders on S3DF): survey the folder(s) the user names.
  `locations.md` becomes the main record.

## 2. Ask once

In one message, ask only for what the survey didn't answer:
- **Sources:** grants, papers, slide decks, or notes for this project. Read them with the matching
  file skill (pdf/docx/pptx).
- **Locations:** where the data and analyses live on each machine; which machines run what.
- **Grant/aim link,** collaborators, planned papers and talks.
- **Sensitivity:** confirm the hub repo is private. If the code repo is or will be public, nothing
  unpublished goes in it. The pointer `AGENTS.md` is the only thing added there.

If the user says "just do it", proceed and leave `TODO(user)` markers.

## 3. Create the project folder in the hub

- `cp -R $HUB/projects/_template $HUB/projects/<name>`, delete `handoffs/TEMPLATE.md` from the copy,
  and fill every file from the survey and sources:
  - `CARD.md`: what it is, repo, machines, grant/aims table, outputs, key results, related projects.
  - `STATUS.md`: the current state. Mark inferences `(inferred)`. The header records machine, agent,
    repo@branch SHA.
  - `TODO.md`: seed from TODO/FIXME comments, unfinished aims, and the user's notes. Tag machines.
  - `DECISIONS.md`: decisions visible in the sources or git history.
  - `methods.md`: data, pipeline (pointing to code paths), pitfalls, validation.
  - `locations.md`: code, input data, and every known analysis/output with machine + path +
    producing repo@commit/script/job.
- Delete template sections that don't apply rather than leaving them empty.

## 4. Register it

- Add or update the project's row in `$HUB/PROJECTS.md`, linking to `projects/<name>/CARD.md`.
- Add a line to `$HUB/repos.conf` (`projects/<name>  <git URL>  <machines>`) if there's a code repo.
- If the project needs a machine that isn't in `machines.md`, add a section for it (with TODOs).

## 5. Distill the science

- **Shared** material (applies to several projects: grants, the program overview, glossary, literature)
  goes in `$HUB/grants/<grant>/{source,aims}.md`, `$HUB/science/`, and `$HUB/literature/`.
- **Project-specific** material goes in `projects/<name>/CARD.md` and `methods.md`.
- For each source: put a markdown extract in `$HUB/grants/<grant>/source.md` (or
  `science/sources/<short-name>.md` for non-grant documents), with a header giving the original
  filename, date, and storage location. Copy the original to `$HUB/originals/`.
- Map each aim to the project(s) that serve it, in both directions: `grants/<grant>/aims.md` ↔ the
  `CARD.md` aims table.
- Where sources disagree, prefer the newer one, log it in `DECISIONS.md`, and flag it for the user.
- Keep the tone factual: no grant marketing language unless it's quoted.

## 6. Point the code repo at the hub

In the code repo, create or merge a short `AGENTS.md` using
[references/templates.md](references/templates.md): how to build, test, and run, plus the pointer
to `$HUB/projects/<name>/` and the session protocol. Keep it **≤ ~60 lines**, with no progress or
state. Add `CLAUDE.md` containing `@AGENTS.md`. If the repo has old `docs/agent/` state files,
migrate their content into the hub and leave a one-line note pointing there.

Optionally suggest that the user add the hub to Claude Code's `additionalDirectories` for this repo,
so agents can write to it.

## 7. Write the first handoff

`projects/<name>/handoffs/YYYY-MM-DD-HHMM-<machine>-<agent>.md`, following
`_template/handoffs/TEMPLATE.md`, describing this setup session. Use the real current time (`date`).

## 8. Verify

- Every path in `CARD.md`, `locations.md`, and the code repo's `AGENTS.md` exists, or is marked as
  living on another machine.
- `$HUB/sync.sh status` lists the repo.
- No secrets, tokens, passwords, or raw data in any file. Originals are only in `originals/`.
- Every science claim has a `[src: ...]` tag or a `TODO(verify)` marker.

## 9. Save and report

- Show the user the hub diff and the code-repo diff. On their OK, run
  `$HUB/sync.sh save "<name>: project overview"`. Commit the code repo only if they ask.
- Report: files created or changed, the `TODO(user)` / `TODO(verify)` items that need their input, and
  the habit that makes this work: `prompts/start.md` at the start and `prompts/end.md` at the end of
  every session, on any machine.

## Refreshing an existing project

When `projects/<name>/` already exists:
- Re-survey: read the handoffs newer than `STATUS.md`, `git log` since the SHA in `STATUS.md`, and any
  new output directories.
- Rewrite `STATUS.md`, prune `TODO.md` (move finished items to Done), add missing `locations.md`
  entries, and flag anything in `CARD.md`/`methods.md` the code no longer matches.
- If `handoffs/` has more than ~30 files, summarize the oldest into `handoffs/ARCHIVE.md` and delete
  them (git history keeps them). Ask first.
- Write a handoff for the refresh, show a diff summary, and save.

## Standalone mode (no hub)

If the user doesn't want a hub for this project, put the same project files in the code repo
under `docs/agent/` (the same names, with `handoffs/` inside), put science context in `science/`, and
make the repo's `AGENTS.md` point there instead. Everything else stays the same.
