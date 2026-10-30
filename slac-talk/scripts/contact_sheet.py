"""Tile slide renders into labelled contact sheets (12 per sheet at 4 columns), to look at many slides at once.

Usage: python3 contact_sheet.py render_dir out_prefix [columns]
Writes out_prefix-1.jpg, out_prefix-2.jpg, ... and prints their absolute paths (open them with the Read tool).
"""
import glob
import os
import sys

from PIL import Image, ImageDraw

d, prefix = sys.argv[1], sys.argv[2]
cols = int(sys.argv[3]) if len(sys.argv) > 3 else 4
fs = sorted(glob.glob(os.path.join(d, "*.png")))
per, W = cols * 3, 700
for k in range(0, len(fs), per):
    ims = [Image.open(f).convert("RGB") for f in fs[k:k + per]]
    h = int(W * ims[0].height / ims[0].width)
    sheet = Image.new("RGB", (cols * (W + 10), ((len(ims) - 1) // cols + 1) * (h + 30)), "white")
    dr = ImageDraw.Draw(sheet)
    for i, im in enumerate(ims):
        x, y = (i % cols) * (W + 10), (i // cols) * (h + 30)
        sheet.paste(im.resize((W, h)), (x, y + 25))
        dr.text((x + 5, y + 5), os.path.splitext(os.path.basename(fs[k + i]))[0], fill="black")
    out = f"{prefix}-{k // per + 1}.jpg"
    sheet.save(out, quality=85)
    print(os.path.abspath(out))
