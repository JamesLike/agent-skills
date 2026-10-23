---
name: write-to-pdf
description: "Generate PDFs on S3DF using reportlab (pandoc not available). Use when converting markdown files to PDF, creating shift summary reports, or generating any formatted PDF document. Covers markdown→PDF conversion, custom two-column layouts, white background, code blocks, tables, and bullet lists."
---

# Skill: write-to-pdf

Generate PDFs on S3DF using **reportlab** (pandoc is not available on S3DF).
Python interpreter to use: `/sdf/home/f/fpoitevi/miniconda3/bin/python3`

---

## Quick Start

### Convert a markdown file to PDF
```bash
/sdf/home/f/fpoitevi/miniconda3/bin/python3 \
  /sdf/home/f/fpoitevi/.claude/skills/write-to-pdf/scripts/md_to_pdf.py \
  input.md [output.pdf]
```

If `output.pdf` is omitted, it writes `input.pdf` alongside the input file.

### Convert beam_notes.md
```bash
/sdf/home/f/fpoitevi/miniconda3/bin/python3 \
  /sdf/home/f/fpoitevi/.claude/skills/write-to-pdf/scripts/md_to_pdf.py \
  /sdf/data/lcls/ds/mfx/mfx101609126/results/fpoitevi/beam_notes.md \
  /sdf/data/lcls/ds/mfx/mfx101609126/results/fpoitevi/beam_notes.pdf
```

---

## Supported Markdown Features

| Element | Syntax |
|---------|--------|
| Headings | `#` `##` `###` `####` |
| Bold / italic / bold-italic | `**b**` `*i*` `***bi***` |
| Inline code | `` `code` `` |
| Fenced code blocks | ` ``` ` ... ` ``` ` |
| Bullet lists (2 levels) | `- item` / `  - nested` |
| Pipe tables | `\| col \| col \|` |
| Horizontal rules | `---` |
| Links | `[text](url)` → rendered as text only |

---

## Custom Report Generation

For custom two-column layouts (e.g. shift summaries), write a Python script
that imports from `md_to_pdf.py` or uses reportlab directly.

### Key patterns

#### White background (always include this)
```python
from reportlab.platypus import SimpleDocTemplate
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors

class WhiteBG(SimpleDocTemplate):
    def handle_pageBegin(self):
        self.canv.setFillColor(colors.white)
        self.canv.rect(0, 0, letter[0], letter[1], fill=1, stroke=0)
        super().handle_pageBegin()
```

#### Two-column layout
```python
from reportlab.platypus import Table, TableStyle

col_table = Table([[col1_flowables, col2_flowables]],
                  colWidths=[3.55*inch, 3.55*inch])
col_table.setStyle(TableStyle([
    ('VALIGN',      (0,0), (-1,-1), 'TOP'),
    ('LEFTPADDING', (0,0), (-1,-1), 4),
    ('RIGHTPADDING',(0,0), (-1,-1), 4),
    ('LINEAFTER',   (0,0), (0,-1),  0.5, colors.HexColor('#cccccc')),
]))
```

#### Paragraph styles
```python
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT

h1 = ParagraphStyle('h1', fontSize=11, fontName='Helvetica-Bold',
                    textColor=colors.HexColor('#1a3a6b'), spaceBefore=8, spaceAfter=3)
body = ParagraphStyle('body', fontSize=8.5, fontName='Helvetica', spaceAfter=3, leading=12)
bullet = ParagraphStyle('bullet', fontSize=8.5, fontName='Helvetica',
                        spaceAfter=1.5, leading=11, leftIndent=12, bulletIndent=2)
code = ParagraphStyle('code', fontSize=7.5, fontName='Courier',
                      backColor=colors.HexColor('#f4f4f4'), leftIndent=12)
```

#### Preformatted code block
```python
from reportlab.platypus import Preformatted
Preformatted("some code\nmore code", code_style)
```

---

## Gotchas

- **Transparent background** — reportlab PDFs have no background by default; always use the `WhiteBG` subclass above or the background will appear transparent in some viewers.
- **No HTML tags in Paragraph text** — use reportlab XML subset only: `<b>`, `<i>`, `<font face="..." size="...">`, `<br/>`. Escape `&` → `&amp;`, `<` → `&lt;`, `>` → `&gt;`.
- **Preformatted vs Paragraph for code** — use `Preformatted` for multi-line code blocks (preserves whitespace); use `<font face="Courier">` inline for single-line inline code in a `Paragraph`.
- **Table column widths must sum to page width minus margins** — letter width = 8.5 in; with 0.65 in margins each side, usable = 7.2 in.
- **reportlab is in miniconda3** — use `/sdf/home/f/fpoitevi/miniconda3/bin/python3`, not the psana conda env (reportlab not installed there).

---

## Files

| File | Purpose |
|------|---------|
| `scripts/md_to_pdf.py` | Standalone markdown→PDF converter |
| `SKILL.md` | This file |

## Example outputs
- `results/fpoitevi/beam_notes.pdf` — shift log converted from markdown
- `results/fpoitevi/shift_summary_jun24_27.pdf` — custom two-column shift summary
- `results/fpoitevi/shift_summary.py` — source for the shift summary report
