# Templates

Replace `<...>` placeholders. Delete sections that don't apply rather than leaving them empty.

---

## AGENTS.md

```markdown
# <Project name>

<One paragraph: what scientific question this serves, what the code does, and who uses it.>

## Where things live
- Science context: `science/OVERVIEW.md` (start here), `science/aims.md`, `science/glossary.md`, `science/methods.md`
- Literature: `science/literature/` + `references.bib`
- Code: `src/<pkg>/` · Tests: `tests/` · Analysis/figure scripts: `analysis/`
- Papers: `papers/<name>/` · Talks: `talks/<name>/`
- Current state: `docs/agent/STATUS.md` · Last session: `docs/agent/HANDOFF.md` · Why we did things: `docs/agent/DECISIONS.md`
- To-dos: `TODO.md` <or: GitHub Issues — use `gh issue list`>

## Read before…
- **coding** → this file + `STATUS.md`
- **analysis** → `science/methods.md` + `science/glossary.md`
- **writing papers/talks/grants** → `science/OVERVIEW.md`, `science/aims.md`, `science/glossary.md`, relevant `science/literature/` notes

## Environments
### <Local: e.g. macOS laptop>
- Purpose: <dev, small tests, writing>
- Env: `<conda activate ...>` · Test data: `<path>`
### <Cluster: e.g. S3DF / psana>
- Purpose: <full-data analysis, production runs>
- Data (read-only): `<path>` · Scratch/output: `<path>`
- Env: `<activation command>`
- Jobs: `sbatch <script>`. **Never run heavy work on login nodes.**
- Limits: <no internet on compute nodes, quotas, etc.>

## Rules
- Run tests with `<command>` before committing code.
- Every figure/number in a paper comes from a script in `analysis/`; never hand-edit figures.
- Don't commit data or large outputs; reference their paths instead.
- Don't invent scientific claims; cite `science/` or literature, or ask.
- <style/lint rules, naming conventions>

## Session protocol
- Start: follow `docs/agent/prompts/start.md`
- End: follow `docs/agent/prompts/end.md`
```

---

## CLAUDE.md

```markdown
@AGENTS.md
```

---

## science/OVERVIEW.md

```markdown
# Scientific overview
_Last reviewed: <date> · Sources: <short-names>_

## The question
<1–3 sentences.> [src: ...]

## Why it matters
<Significance, gap in the field.> [src: ...]

## Central hypotheses
1. <H1> [src: ...]

## Approach in brief
<Experiment/facility/data → analysis → expected outcome. Links to methods.md.>

## Current best understanding
<What results so far suggest. Mark (preliminary) where applicable.>

## Open questions
- <...>
```

---

## science/aims.md

```markdown
# Aims
_Source of truth for what this project promised to deliver._

| Aim | Sub-aim | Deliverable | Code / analysis | Status |
|---|---|---|---|---|
| 1. <title> | 1a. <...> | <paper, dataset, tool> | `analysis/...` | not started / in progress / done |

## Aim 1 — <title>
<Short description, success criteria, risks/alternatives.> [src: ...]
```

---

## science/glossary.md

```markdown
# Glossary & conventions
| Term / symbol | Meaning | Units | Notes / code name |
|---|---|---|---|
| <q> | <momentum transfer> | Å⁻¹ | `q` in `src/...` |
```

---

## science/methods.md

```markdown
# Methods
## Data
<Facilities, instruments, run/experiment IDs, formats, where stored.>
## Processing pipeline
<Steps, with links to code.>
## Known pitfalls
- <e.g. detector calibration drift across runs X–Y>
## Validation
<How we know results are right: tests, simulations, cross-checks.>
```

---

## science/literature/README.md

```markdown
# Literature notes
One file per key paper: `<firstauthor><year>-<keyword>.md`. BibTeX keys match `references.bib`.

Template per note:
- **Cite key:** <key>
- **Claim:** <one sentence>
- **Method:** <one sentence>
- **Relevance to us:** <supports / contradicts / method we reuse>
```

---

## science/sources/<short-name>.md

```markdown
# <Document title> (extract)
- Original: `<filename>`, <date>, stored at <Box/Drive/LFS path>
- Type: <grant / talk / paper / notes>
- Extracted: <date>. Key sections only; not the full document.

## <Section>
<Condensed content>
```

---

## TODO.md

```markdown
# TODO
_Tags: [local] [s3df] [blocked] · owner initials if shared_

## Code
- [ ] <...>
## Analysis
- [ ] <...> [s3df]
## Writing (papers / talks / grants)
- [ ] <...>
## Infra
- [ ] <...>

## Done (recent)
- [x] <...> (<date>)
```

---

## docs/agent/STATUS.md

```markdown
# Status
_Updated: <date> on <machine>_

## Works
- <...>
## Broken / in progress
- <...>
## Next up
1. <...>
```

---

## docs/agent/HANDOFF.md

Newest entry first; keep about the last 10 entries and trim older ones.

```markdown
# Handoff log

## <date> · <machine> · <agent/tool>
- **Did:** <...>
- **Left open:** <...>
- **Next step (exact):** <command or task>
- **Jobs running:** <SLURM job IDs, output paths> / none
```

---

## docs/agent/DECISIONS.md

```markdown
# Decisions
## <date> — <short title>
- **Decision:** <...>
- **Why:** <...>
- **Alternatives rejected:** <...>
```

---

## docs/agent/prompts/start.md

```markdown
Start of session. Do this before any other work:
1. `git pull`, then `git status` and `git log --oneline -15`.
2. Read AGENTS.md, docs/agent/STATUS.md, and the top entry of docs/agent/HANDOFF.md.
3. Identify which environment you are on (see AGENTS.md › Environments) and say so.
4. Check any jobs listed as running in HANDOFF.md (`squeue -u $USER` / output paths).
5. Summarize in ≤5 bullets where things stand and propose the next step. Wait for confirmation.
```

---

## docs/agent/prompts/end.md

```markdown
End of session:
1. Update docs/agent/STATUS.md.
2. Add a new top entry to docs/agent/HANDOFF.md (date, machine, did, left open, exact next step, running jobs).
3. Append any decisions made to docs/agent/DECISIONS.md.
4. Update TODO.md (check off done items, add new ones) and the status column in science/aims.md if it changed.
5. If scientific understanding changed, update science/OVERVIEW.md › Current best understanding.
6. Show me the diff, then commit with a descriptive message and push once I confirm.
```
