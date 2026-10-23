# Templates

**Hub project files** (CARD, STATUS, TODO, DECISIONS, methods, locations, handoff) are maintained in
the hub itself, in `~/projects/research-hub/projects/_template/`. Copy them from there so there's a
single source of truth. The only template kept here is the code repo's pointer file.

---

## Code repo: AGENTS.md

```markdown
# <name>

<One or two sentences: what this code does.>

## Context, progress, and handoffs: research-hub
This repo holds code only. All agent context lives in the hub:
`~/projects/research-hub/projects/<name>/`. Read `STATUS.md` and the newest `handoffs/` there
before working. Machine-specific paths and environments are in `~/projects/research-hub/machines.md`.
(Hub not present? `git clone git@github.com:JamesLike/research-hub.git ~/projects/research-hub`)

## Session protocol
- Start: follow `~/projects/research-hub/prompts/start.md` for project `<name>`
- End: follow `~/projects/research-hub/prompts/end.md`; the hub must be pushed before you stop

## Layout
- `src/<pkg>/`: <...> · `tests/`: <...> · `analysis/`: scripts that make figures and numbers
- <other key dirs>

## Build / test / run
- Env: `<conda env create -f environment.yml && conda activate ...>`
- Test: `<pytest -q>`
- Run on S3DF: `<sbatch scripts/...>`. Never run heavy work on login nodes

## Rules
- Run tests before committing code
- Don't commit data or large outputs; record their paths in the hub's `locations.md`
- Every figure or number used in a paper comes from a script in `analysis/`
- <style / lint / naming conventions>
```

---

## Code repo: CLAUDE.md

```markdown
@AGENTS.md
```

---

## Optional: Claude Code access to the hub

Code repo `.claude/settings.json` (or `.claude/settings.local.json` to keep it uncommitted):

```json
{
  "permissions": {
    "additionalDirectories": ["/Users/<user>/projects/research-hub"]
  }
}
```

Use the absolute path for each machine (`echo ~/projects/research-hub`). Prefer
`settings.local.json`, since the path differs between the mac and S3DF.
