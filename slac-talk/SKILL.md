---
name: slac-talk
description: Build PowerPoint talks on the SLAC/Stanford template in James Baxter's presenting style (cardinal Lato titles, progressive build slides, a red takeaway at the end of each build, figure-first slides, elevator-pitch quadrants, backup slides). Use this whenever James asks for slides, a deck, a talk, a presentation, an LDRD pitch, a group-meeting or collaborator update, an SAC or R&D briefing, or wants to turn notebook results, research-hub notes or an old deck into a presentation — even if he doesn't say "SLAC template" or "my style". Also use it to update or extend a deck built this way.
---

# SLAC talk in James's style

You're making a talk James will give at SLAC. The output is a `.pptx` on the SLAC FY27 template, built by a small Python
script kept next to the talk so it can be rebuilt as results change (results in his projects change daily).

Read `references/style.md` before outlining: it describes his style, the slide patterns, and the narrative arcs.
The library `scripts/slac_deck.py` implements those patterns; its docstring shows usage.

## Workflow

1. **Pin down the talk.** Audience and venue (LDRD panel, group meeting, collaborators, SAC), length, the one message,
   and where the material lives. If he hasn't said, assume a ~20-minute technical update, say so, and carry on.
   LDRD talks follow the template's section list and timing (see style.md §1).

2. **Gather the content from the source of truth, not memory.**
   - Project context: for projects in the research hub, read `~/projects/research-hub/projects/<name>/` (STATUS, newest
     handoffs, NOTES with the numbers). `git pull` the hub and `git fetch` the code repo first — he often says "there are updates".
   - Notebook figures: `python3 scripts/notebook_figs.py nb.ipynb figdir` extracts every PNG output labelled by its section
     heading. Notebooks on other branches: `git show origin/<branch>:<nb>.ipynb > nb/<nb>.ipynb` first.
   - Figures from his old decks (schematics, cartoons, team photos): `python3 scripts/pptx_media.py deck.pptx outdir 2,19`
     extracts the pictures on those slides with their crops applied. His decks are in `~/Documents/LDRD_slides/` and `~/Downloads/`.
   - Numbers with no figure yet: use native tables or charts (`table`, `line_chart`, `scatter_chart`) rather than skipping them.
   - Never invent a result, number or claim; every number on a slide should trace to a notes section or notebook, and the
     slide's `source` line says which.

3. **Outline before building.** One message per slide; group slides into builds; end each build on a takeaway or a
   rhetorical question that sets up the next one; put caveats where the result is. Share the outline briefly, then build.

4. **Build.** Put the talk in a folder in the relevant project (e.g. `<repo>/talks/YYYY-MM_<topic>/`) with:
   - `build_deck.py` — imports `slac_deck` from this skill (`sys.path.insert(0, os.path.expanduser("~/.claude/skills/slac-talk/scripts"))`),
     composes the slides, saves the `.pptx`. Keep numbers in this script, near the slide that uses them, with a comment or
     `source=` saying where they came from, so a later "update the deck" is a small edit.
   - figure folders it reads (`fig_*`, `ldrd_media/`), and a `.gitignore` for `*.pptx` and those folders if the repo
     shouldn't carry binaries.
   Typical calls: `cover`, `pitch` (4 quadrants), `build(title, [steps], notes=[...], source=...)` with `picture`, `text`
   (strings starting `-` are bullets; lists of `(text, bold)` runs for bold labels), `takeaway`, `callout`, `stat`, `table`,
   charts; `labelled_list` for conclusions; `figure_slide` for backup.

5. **QA — always render and look.**
   - `python3 scripts/render_slides.py deck.pptx /tmp/render [--slides 5,38-51]` then
     `python3 scripts/contact_sheet.py /tmp/render /tmp/sheet 3` and open the sheets with Read. Render only changed slides
     on updates; a full render is ~3 s per slide.
   - Look for: text wrapping into another element (long stat numbers, takeaways over figures), figures too small to read,
     uneven gaps, anything off the slide or over the bottom strip (y > 6.8 in is the logo/citation/number band).
   - Quick Look draws Lato as Times, ignores autofit and renders charts roughly — check chart axes and dashes in the XML,
     not the render, and leave ~10% slack in text boxes.
   - If the pptx skill's `scripts/office/validate.py` is available, run it with `--original assets/SLAC_template_FY27.pptx`.

6. **Hand over.** Give the path to the `.pptx`, the story in a few lines, what's assumed (audience, title-slide names, date),
   which numbers are preliminary or still running, and what Quick Look can't show. Commit only when asked; use his
   attribution lines from the session's system reminder.

## Updating an existing deck
Pull the new results, find the affected slides in its `build_deck.py`, edit in place (replace a build's steps, add slides,
refresh conclusions, next steps and the pitch's "next" quadrant, speaker notes), rebuild, render just those slides.
Stale statements are the usual bug ("running", "queued", "not yet") — grep the script for them.

## Gotchas
- `python-pptx`'s `add_slide` drops the slide-number placeholder; `SlacDeck.content` copies it back.
- Don't use theme accent colours for shapes: interior accent1 is Office blue. Use the hex constants in `slac_deck`.
- Bold-label paragraphs (lists of runs) aren't bulleted; plain `-` strings are.
- Stat values longer than 8 characters drop to 28 pt automatically so they stay on one line; keep them short anyway.
- His Mac has no LibreOffice and PowerPoint automation is blocked, hence the Quick Look renderer.
