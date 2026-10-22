# Personal Claude / agent skills

Private collection of agent skills (`<name>/SKILL.md` format), shared across machines.

## Install on a new machine

```bash
git clone git@github.com:JamesLike/agent-skills.git ~/.claude/skills
```

For OpenCode or other agents that don't read `~/.claude/skills`, point them at the
skill file directly ("follow ~/.claude/skills/<name>/SKILL.md") or symlink the
folder where that tool looks for skills.

## Sync

```bash
cd ~/.claude/skills && git pull            # get updates
git add -A && git commit -m "..." && git push   # share edits
```

## Secrets

Skills that need credentials ship a `config.example.yaml`; copy it to
`config.yaml` on each machine. `config.yaml` is git-ignored.

## Skills

| Skill | Purpose |
|---|---|
| `approval` | Only execute your plan upon my approval… |
| `breakdown` | Break down the questions/tasks in my prompt… |
| `clarify-before-research` | Ask me clarifying questions before research… |
| `clarify` | Ask me clarifying questions if needed… |
| `formalize-plan` | >-… |
| `gaps` | "Assess and identify gaps. Use when you want to find what's missing, incomplete, or unaddressed in code, docs,… |
| `gh-skills` | "Power-user guide for the GitHub CLI (gh). Use when working with: gh api (GraphQL queries, REST pagination, fi… |
| `goal-to-metrics` | "Turn a vague goal into concrete, measurable metrics. Use when someone says 'I want X to be better' and X need… |
| `latent-demand` | "Analyze the conversation to uncover latent demands — broader aspirations or deeper needs the user may not h… |
| `literature-review-helper` | >… |
| `manuscript-developer` | >… |
| `project-overview` | Set up or refresh the shared, tool-agnostic context layer for a research software project so any coding agent … |
| `scientific-code-auditor` | >… |
| `senior-code-reviewer` | >… |
| `taskify` | Instruct agents to create a task list to keep track of things… |
| `writing-style-reviewer` | >… |
| `zotero-citation-integration` | "Citation management via a Zotero library: look up a DOI/PMID/arXiv ID/title in Zotero, format it in JACS styl… |
