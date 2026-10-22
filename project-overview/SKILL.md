---
name: project-overview
description: Set up or refresh the shared, tool-agnostic context layer for a research software project so any coding agent (Claude Code, OpenCode, etc.) on any machine (laptop, S3DF/psana, other clusters) can pick up work. Creates AGENTS.md (index + environments), CLAUDE.md, science/ context distilled from grants, talks and papers, TODO.md, and docs/agent/ state and handoff files. Trigger on requests like "write a project overview", "set up AGENTS.md", "scaffold project context", "make this repo agent-ready", "distill my grant into project context", "set up handoff files", or "refresh the project overview".
---

# Project Overview & Shared Agent Context

Builds a **plain-text, git-tracked context layer** so a project's goals, science, environments, to-dos and progress travel with the repo instead of living in one tool's memory on one machine.

Guiding principles (apply them throughout):

1. **Git is the only shared memory.** Nothing important lives only in `~/.claude`, OpenCode sessions, or chat history.
2. **Layers.** `AGENTS.md` is a short index (about a page). Detail lives in files it points to, which are loaded only when a task needs them.
3. **Distill, don't dump.** A 2-page `aims.md` beats a 40-page grant PDF. Originals stay outside git (or in LFS). Markdown extracts and summaries go in.
4. **Never invent science.** Every claim in `science/` is traceable to a source the user provided, or marked `TODO(verify)`.
5. **Never overwrite silently.** If a file exists, merge into it and show the diff.

Templates for every file are in [references/templates.md](references/templates.md). Read it before writing files.

## Workflow

### 1. Survey what exists

Do this before asking the user anything:

- Repo layout (`git ls-files | head -200`, top-level dirs), README, build/test config (`pyproject.toml`, `setup.py`, `environment.yml`, `Makefile`, CI files, SLURM scripts).
- Existing context files: `AGENTS.md`, `CLAUDE.md`, `.claude/`, `.opencode/`, `docs/`, `TODO*`, `NOTES*`, `CHANGELOG`.
- `git log --oneline -30` for recent direction of work.
- Hints of compute environments: hard-coded paths like `/sdf/...`, `sbatch` headers, conda env names, `psana` imports.

### 2. Collect the soft context

Ask in **one** message, and only for what the survey didn't answer:

- **Sources:** paths to grants, proposals, papers, slide decks, or notes to distill. Accept PDF/DOCX/PPTX/MD and read them with the matching skill.
- **Environments:** each machine or cluster used, with data locations, env activation, job submission, network limits, and what must *not* run where (e.g. heavy jobs on login nodes).
- **Audience & outputs:** planned papers and talks, target venues, collaborators, and whether to use GitHub Issues or `TODO.md` for the backlog.
- **Sensitivity:** whether the repo is private or public. If public or unknown, do **not** put unpublished grant text or results in it. Ask first.

If the user says "just do it", proceed with what's available and leave `TODO(user)` markers.

### 3. Create the structure

Create only what's missing:

```
AGENTS.md                  # index, rules, environments  (≤ ~120 lines)
CLAUDE.md                  # one line: @AGENTS.md
TODO.md                    # unless the user chose GitHub Issues
science/OVERVIEW.md        # question, hypotheses, significance (1–2 pages)
science/aims.md            # aims → sub-aims → deliverables → status
science/glossary.md        # terms, symbols, units, naming conventions
science/methods.md         # approach, data, known pitfalls
science/literature/README.md + references.bib
science/sources/           # markdown extracts of originals (+ pointer to where originals live)
docs/agent/STATUS.md
docs/agent/HANDOFF.md
docs/agent/DECISIONS.md
docs/agent/prompts/start.md
docs/agent/prompts/end.md
```

Add `papers/` or `talks/` folders only if the user has planned outputs. Add `.gitignore` entries for data and large outputs (`*.h5`, `*.xtc2`, `slurm-*.out`, scratch dirs) if they're missing.

### 4. Distill the science

For each source document:

1. Write a markdown extract to `science/sources/<short-name>.md`: the key sections only, with a header stating the original filename, date, and where the original is stored.
2. Fold its content into `OVERVIEW.md`, `aims.md`, `glossary.md` and `methods.md`.
3. Cite inline as `[src: <short-name> §<section>]` so claims can be checked.
4. Where sources disagree (e.g. an old grant vs. a newer talk), prefer the newer one, record the change in `DECISIONS.md`, and flag it for the user.
5. In `aims.md`, map each aim to the code and analysis that serves it (`src/...`, `analysis/...`), or mark `not started`.

Keep tone factual. No marketing language from grants ("transformative", "unprecedented") unless it's quoted as such.

### 5. Write AGENTS.md last

It indexes everything else, so write it after the rest exists. Required sections are in the template: Project in one paragraph, Where things live, Environments, Rules, Session protocol, When writing papers/talks. Every path it mentions must exist.

### 6. Seed state files

- `STATUS.md`: the current state as inferred from the survey and git log. Mark inferences `(inferred)`.
- `TODO.md` (or Issues): seed from TODO/FIXME comments, aims marked `not started`, and anything the user mentioned. Group by area: Code / Analysis / Writing / Infra. Tag a machine where relevant, e.g. `[s3df]`.
- `DECISIONS.md`: start with any decisions visible in the sources or git history.
- `HANDOFF.md`: the first entry is this setup session.

### 7. Verify

- `AGENTS.md` is ≤ ~120 lines, and every referenced path exists (`grep -o` the paths and `test -e` each).
- `CLAUDE.md` is exactly `@AGENTS.md` (plus optional Claude-only notes below it).
- No secrets, tokens, passwords, or personal data in any file.
- Every `science/` claim has a `[src: ...]` tag or a `TODO(verify)` marker.
- `git status` shows only intended files. Do **not** commit unless the user asks.

### 8. Report

Tell the user:

- which files you created or changed, and what you merged into existing ones
- the `TODO(verify)` / `TODO(user)` items needing their input, as a short list
- the two habits that make this work: run `docs/agent/prompts/start.md` at the start of each session and `end.md` at the end, on any machine and with any agent

## Refreshing an existing setup

When the files already exist ("refresh the overview"):

- Re-run steps 1 and 6. Update `STATUS.md` and the status column in `aims.md` from recent commits.
- Prune: move completed TODOs to a `## Done (recent)` section, and flag aims or decisions the code no longer reflects.
- Check that `AGENTS.md` is still short and its paths still resolve.
- Show a diff summary rather than rewriting files wholesale.
