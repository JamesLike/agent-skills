#!/usr/bin/env python3
"""
md_to_pdf.py — Convert a markdown file to PDF using reportlab.
Usage: python3 md_to_pdf.py input.md [output.pdf]

Supports:
  # H1  ## H2  ### H3  #### H4
  - bullet lists (nested with 2- or 4-space indent)
  **bold**  *italic*  `inline code`
  ```code blocks```
  --- horizontal rules
  | table | rows |  (simple pipe tables)
  Blank lines → paragraph breaks
"""

import sys
import re
from pathlib import Path

from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, HRFlowable,
    Table, TableStyle, Preformatted
)
from reportlab.lib.enums import TA_LEFT, TA_CENTER

# ── Styles ────────────────────────────────────────────────────────────

BLUE   = colors.HexColor('#1a3a6b')
GREY   = colors.HexColor('#555555')
LGREY  = colors.HexColor('#dddddd')
BLACK  = colors.HexColor('#111111')
GREEN  = colors.HexColor('#1a7a1a')
RED    = colors.HexColor('#c0392b')
ORANGE = colors.HexColor('#e67e00')
CODE_BG= colors.HexColor('#f4f4f4')

def make_styles():
    return {
        'h1':    ParagraphStyle('h1',    fontSize=13, fontName='Helvetica-Bold',
                                textColor=BLUE, spaceBefore=10, spaceAfter=3,
                                borderPad=2, borderWidth=0, leading=16),
        'h2':    ParagraphStyle('h2',    fontSize=11, fontName='Helvetica-Bold',
                                textColor=BLUE, spaceBefore=8, spaceAfter=2, leading=14),
        'h3':    ParagraphStyle('h3',    fontSize=9.5, fontName='Helvetica-Bold',
                                textColor=BLUE, spaceBefore=6, spaceAfter=2, leading=12),
        'h4':    ParagraphStyle('h4',    fontSize=9, fontName='Helvetica-BoldOblique',
                                textColor=GREY, spaceBefore=4, spaceAfter=1, leading=11),
        'body':  ParagraphStyle('body',  fontSize=8.5, fontName='Helvetica',
                                textColor=BLACK, spaceAfter=3, leading=12),
        'bullet':ParagraphStyle('bullet',fontSize=8.5, fontName='Helvetica',
                                textColor=BLACK, spaceAfter=1.5, leading=11,
                                leftIndent=12, bulletIndent=2),
        'bullet2':ParagraphStyle('bullet2',fontSize=8.5, fontName='Helvetica',
                                textColor=BLACK, spaceAfter=1.5, leading=11,
                                leftIndent=24, bulletIndent=14),
        'code':  ParagraphStyle('code',  fontSize=7.5, fontName='Courier',
                                textColor=BLACK, spaceAfter=1, leading=10,
                                leftIndent=12, backColor=CODE_BG),
        'hr':    None,
    }

# ── Inline markup ─────────────────────────────────────────────────────

def inline(text):
    """Convert **bold**, *italic*, `code` to reportlab XML."""
    # escape XML special chars first (except those we're about to add)
    text = text.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
    # bold+italic
    text = re.sub(r'\*\*\*(.+?)\*\*\*', r'<b><i>\1</i></b>', text)
    # bold
    text = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', text)
    # italic
    text = re.sub(r'\*(.+?)\*', r'<i>\1</i>', text)
    # inline code
    text = re.sub(r'`([^`]+)`', r'<font face="Courier" size="7.5">\1</font>', text)
    # markdown links [text](url) → just text
    text = re.sub(r'\[([^\]]+)\]\([^\)]+\)', r'\1', text)
    return text

# ── Parser ────────────────────────────────────────────────────────────

def parse(md_text, styles):
    story = []
    lines = md_text.splitlines()
    i = 0

    def add(flowable):
        story.append(flowable)

    while i < len(lines):
        line = lines[i]

        # fenced code block
        if line.strip().startswith('```'):
            i += 1
            code_lines = []
            while i < len(lines) and not lines[i].strip().startswith('```'):
                code_lines.append(lines[i])
                i += 1
            i += 1  # skip closing ```
            if code_lines:
                text = '\n'.join(code_lines)
                add(Preformatted(text, ParagraphStyle(
                    'pre', fontSize=7.5, fontName='Courier',
                    leading=10, leftIndent=12, spaceAfter=4,
                    backColor=CODE_BG, textColor=BLACK
                )))
            continue

        # horizontal rule
        if re.match(r'^-{3,}$', line.strip()) or re.match(r'^\*{3,}$', line.strip()):
            add(HRFlowable(width='100%', thickness=0.5, color=LGREY,
                           spaceBefore=4, spaceAfter=4))
            i += 1
            continue

        # headings
        m = re.match(r'^(#{1,4})\s+(.*)', line)
        if m:
            level = len(m.group(1))
            text  = inline(m.group(2))
            key   = f'h{level}' if level <= 4 else 'h4'
            add(Paragraph(text, styles[key]))
            i += 1
            continue

        # pipe table
        if '|' in line and line.strip().startswith('|'):
            table_lines = []
            while i < len(lines) and '|' in lines[i]:
                table_lines.append(lines[i])
                i += 1
            # filter separator rows
            rows = []
            for tl in table_lines:
                cells = [c.strip() for c in tl.strip().strip('|').split('|')]
                if all(re.match(r'^[-: ]+$', c) for c in cells):
                    continue
                rows.append([Paragraph(inline(c), styles['body']) for c in cells])
            if rows:
                t = Table(rows, hAlign='LEFT')
                t.setStyle(TableStyle([
                    ('FONTNAME',  (0,0), (-1,0), 'Helvetica-Bold'),
                    ('FONTSIZE',  (0,0), (-1,-1), 8),
                    ('GRID',      (0,0), (-1,-1), 0.4, LGREY),
                    ('BACKGROUND',(0,0), (-1,0), colors.HexColor('#e8edf5')),
                    ('VALIGN',    (0,0), (-1,-1), 'TOP'),
                    ('TOPPADDING',(0,0), (-1,-1), 2),
                    ('BOTTOMPADDING',(0,0),(-1,-1), 2),
                    ('LEFTPADDING', (0,0),(-1,-1), 4),
                ]))
                add(t)
                add(Spacer(1, 4))
            continue

        # bullet (- or *)
        m = re.match(r'^(\s*)([-*])\s+(.*)', line)
        if m:
            indent = len(m.group(1))
            text   = inline(m.group(3))
            style  = styles['bullet2'] if indent >= 2 else styles['bullet']
            add(Paragraph(f'• {text}', style))
            i += 1
            continue

        # blank line
        if line.strip() == '':
            add(Spacer(1, 3))
            i += 1
            continue

        # normal paragraph
        add(Paragraph(inline(line), styles['body']))
        i += 1

    return story

# ── Document builder ──────────────────────────────────────────────────

class WhiteBG(SimpleDocTemplate):
    def handle_pageBegin(self):
        self.canv.setFillColor(colors.white)
        self.canv.rect(0, 0, letter[0], letter[1], fill=1, stroke=0)
        super().handle_pageBegin()

def convert(input_path, output_path=None):
    input_path  = Path(input_path)
    output_path = Path(output_path) if output_path else input_path.with_suffix('.pdf')

    md_text = input_path.read_text(encoding='utf-8')
    styles  = make_styles()
    story   = parse(md_text, styles)

    doc = WhiteBG(
        str(output_path),
        pagesize=letter,
        leftMargin=0.65*inch, rightMargin=0.65*inch,
        topMargin=0.55*inch,  bottomMargin=0.55*inch,
    )
    doc.build(story)
    print(f"Written: {output_path}")
    return output_path

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python3 md_to_pdf.py input.md [output.pdf]")
        sys.exit(1)
    inp = sys.argv[1]
    out = sys.argv[2] if len(sys.argv) > 2 else None
    convert(inp, out)
