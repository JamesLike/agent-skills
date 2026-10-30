"""Render slides to PNG with macOS Quick Look, for visual QA when LibreOffice isn't installed.

Usage: python3 render_slides.py deck.pptx outdir [--slides 5,38-51] [--size 1400]
Writes outdir/s<NNN>.png (NNN = slide number). Quick Look only renders a deck's first slide, so each requested
slide is moved to the front of a temporary copy and thumbnailed (~2–4 s per slide).

Known Quick Look differences from PowerPoint: Lato renders as Times (text fit is approximate), text autofit is
ignored, native charts are drawn roughly (sparse axis labels, dashed lines solid), and slide-number fields show
'‹#›'. Trust the XML for those, not the render.
"""
import argparse
import os
import re
import shutil
import subprocess
import tempfile
import zipfile


def parse_slides(spec, n):
    if not spec:
        return list(range(1, n + 1))
    out = []
    for part in spec.split(","):
        a, _, b = part.partition("-")
        out += list(range(int(a), int(b or a) + 1))
    return [k for k in out if 1 <= k <= n]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("deck")
    ap.add_argument("outdir")
    ap.add_argument("--slides", default="")
    ap.add_argument("--size", type=int, default=1400)
    a = ap.parse_args()
    os.makedirs(a.outdir, exist_ok=True)
    z = zipfile.ZipFile(a.deck)
    pres = z.read("ppt/presentation.xml").decode("utf8")
    m = re.search(r"(<p:sldIdLst>)(.*?)(</p:sldIdLst>)", pres, re.S)
    ids = re.findall(r"<p:sldId [^>]*/>", m.group(2))
    tmp = tempfile.mkdtemp()
    try:
        for k in parse_slides(a.slides, len(ids)):
            sid = ids[k - 1]
            order = [sid] + [x for x in ids if x is not sid]
            newp = pres[: m.start(2)] + "".join(order) + pres[m.end(2):]
            fn = os.path.join(tmp, f"s{k:03d}.pptx")
            with zipfile.ZipFile(fn, "w", zipfile.ZIP_STORED) as w:
                for it in z.infolist():
                    data = newp.encode("utf8") if it.filename == "ppt/presentation.xml" else z.read(it.filename)
                    w.writestr(it.filename, data)
            subprocess.run(["qlmanage", "-t", "-s", str(a.size), "-o", tmp, fn],
                           stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=120)
            png = fn + ".png"
            if os.path.exists(png):
                shutil.move(png, os.path.join(a.outdir, f"s{k:03d}.png"))
            else:
                print("no render for slide", k)
            os.remove(fn)
        print("rendered to", os.path.abspath(a.outdir))
    finally:
        shutil.rmtree(tmp)


if __name__ == "__main__":
    main()
