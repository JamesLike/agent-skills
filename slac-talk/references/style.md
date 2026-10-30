# James Baxter's SLAC/Stanford slide style

Distilled from his finalized decks: FY27 LDRD `~/Documents/LDRD_slides/convergent_final.pptx` (= `J_Baxter.pptx`),
FY26 LDRD `BaxterSLAC_LDRD_FY26_final.pptx`, the SAC posters (`~/Documents/sac_virtual_poster_updated_final.pptx`) and
the CBSFX analysis update (`~/projects/convergent-sfx/talks/2026-10_cbsfx_analysis/`, built with this skill's library).
`MFX-HE Flagship Overview SAC - Final.pptx` (Leland Gee) and `Aquila_SLAC_LDRD_FY24_final.pptx` (Andy Aquila) use the
same template but are colleagues' decks, not his style.

## Contents
1. Template
2. How he uses it
3. Slide patterns
4. Narrative arcs
5. Writing on slides
6. Posters

## 1. Template
- File: `assets/SLAC_template_FY27.pptx` (copy of `~/Downloads/SLAC_LDRD_Presentation_Template_FY27.pptx`), 16:9, 13.33 × 7.5 in.
- Masters "SLAC Covers/Title Slides" (13 cover layouts) and "SLAC Interior Slides" (text, columns, agenda, photo, section breaks).
- Font Lato everywhere. Colours: cardinal `8C1515` (titles, cover headline, table headers), accent `B83A4B` (bullets, the
  rule under titles, subtitle text), body black. The interior theme's accent1 is Office blue `4472C4`: never use scheme
  accent colours for callouts, use explicit hex (`slac_deck` does).
- "Text Slide - 1 Column": title at (0.88, 0.29), 11.54 × 0.69 in, 32 pt cardinal with a thin accent rule; optional 20 pt
  accent subtitle at y 1.21; SLAC logo bottom left, slide number bottom right (11 pt).
- Cover "1_Title Slide - Option 4C - Printable": grey background with molecule graphic, SLAC and Stanford/DOE logos;
  placeholders 10 (headline, 48 pt cardinal), 11 (category line), 12 (presenter), 13 (collaborators / date).
- The template's own first slides are LDRD guidance: 17 min talk (~12–14 slides) + 13 min Q&A; sections elevator pitch (1),
  background (2), questions and hypotheses (2), approach (3–4), anticipated results and impact (2), roadmap beyond the LDRD
  (1–2), budget brief (1 table: FY labour / M&S / travel / total, % effort), funding alignment (2, hidden backup).

## 2. How he uses it
- **Two layouts only**: ~95% "Text Slide - 1 Column", plus the Option 4C cover. The cover doubles as a section divider in long talks.
  He does not use the agenda, section-break or photo layouts.
- **Progressive builds from duplicated slides, not animations.** His signature: an idea runs over 2–8 slides with the same
  title, each adding one figure, panel, sentence or callout. Almost no animations, no transitions. So a 17-minute talk is
  40–60 slide files; count build steps as one slide when sizing the talk.
- **Figure first, few words**: ~2 pictures per slide, many figure-only slides; mostly his own schematics (k-vector/Ewald
  diagrams, source → object → detector cartoons, pixel-grid phantoms), simulation panels and matplotlib plots, plus a few
  playful cartoon illustrations.
- **The takeaway comes last, at the bottom**: each build ends with a short red line (`C00000`) or an accent-outlined
  callout box. Often a rhetorical hook into the next section: "If this is so easy why are people not already doing it?",
  "So why stop at 13 mrad?", "But: stage 2 still ended below the merge".
- **Citations** small (11–12 pt) at the bottom left beside the logo: "Journal vol, page (year)"; for his own results the
  source notebook or notes section ("idxscan_ana.ipynb · NOTES §9g"). Image credits as bare names ("James Holton").
- **Backup slides after the conclusions**: alternate versions, extra figures, derivations; FY26 had 8 hidden slides.
- **Speaker notes** occasionally, conversational ("Want to highlight why we are uniquely placed...").

## 3. Slide patterns (all in `scripts/slac_deck.py`)
- **Elevator-pitch quadrants** (`pitch`): on the grey cover background, a cardinal cross splits the slide into
  The problem / The technical advancement / Impact / Delivery-outlook (or question / what we did / result / next), revealed
  one quadrant per slide, each with a bold header, a bold lead sentence and one illustration.
- **Build with takeaway** (`build` + `takeaway` / `callout`): the default content slide.
- **Stat cards** (`stat`): three big cardinal numbers across the top with a one-line label each, for headline numbers.
- **Native tables** (`table`): cardinal header row, white body, one highlighted row in bold cardinal; budget tables use FY
  columns plus Total in $k, then bold-label bullets for Effort / Resources / M&S.
- **Native charts** (`line_chart`, `scatter_chart`): when the numbers exist but no figure does; dashed series for reference
  lines (e.g. "merge"), cardinal for the headline series, greys/soft red for the rest.
- **Process / phases** (`process`): a tinted band of rounded boxes joined by arrows (FY27 "Project overview",
  a method pipeline); one band per phase, revealed as a build.
- **Team grid**: headshots with name, institution, role underneath, institution logos at the end (FY27 "Project team").
- **Conclusions** (`labelled_list`): cardinal bold section labels, e.g. What works / Headline results / Barriers / Caveats,
  or Deliverables / Key risks → mitigations / Headline impact / Future opportunities.
- **Backup figure slides** (`figure_slide`): "Backup: ..." title, one big figure, grey caption, source line.

## 4. Narrative arcs
- **LDRD / proposal**: hook or elevator pitch → challenge (why current methods fall short) → background built from first
  principles → "X as a solution" → simulations or preliminary evidence → "Problems to solve" → approach / project phases →
  team → impact and opportunities → budget → conclusions → backup. Follow the template's section list and timing.
- **Results update** (group meeting, collaborators): pitch quadrants → recap of the idea (reuse his LDRD schematics) →
  setup (what was simulated / measured, and how it's scored) → the first failure and its cause → each fix as a build ending
  in a takeaway → headline result with caveats → what's now the barrier → conclusions with bold labels → next steps → backup.
- One message per slide; titles carry it ("Merged data are better at every divergence").

## 5. Writing on slides
- Titles: "Topic: subtopic" kept identical through a build ("Background: Serial Femtosecond Crystallography (SFX)"), or the
  claim itself ("Main Impact: 5-20x Lower sample consumption"). No full stop.
- Short bullet fragments, 14–20 pt (24 pt on sparse slides); bold labels for key phrases ("The Problem:", "Phase 1").
- Numbers with the comparison inline: "100 / 100 / 94% at 7 / 10 / 13 mrad (pipeline 43 / 18 / 1%)".
- Keep caveats visible on results slides (preliminary, simulation only, sample size) — he presents contested results
  (e.g. CBSFX gain 14× vs 3–4×) carefully, and his project rules forbid unsupported claims.
- No decorative bars, no accent lines beyond the template's own title rule, no gradients.

## 6. Posters (SAC, 48 × 36 in)
SLAC poster template (banner with SLAC and DOE logos top right), not the deck template: title in bold red, author list with
numbered affiliations, five numbered section headers ("1. Imaging with entangled photons..."), dense bullets and figures,
grant acknowledgement at the bottom. Build posters by editing the poster file directly, not with `slac_deck`.
