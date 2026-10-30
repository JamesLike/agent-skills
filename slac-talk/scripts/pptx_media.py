"""Pull the pictures off chosen slides of an existing deck, with PowerPoint's crop applied, so old figures
(schematics, cartoons, team photos) can be reused in a new talk.

Usage: python3 pptx_media.py deck.pptx outdir 2,5,19     (slide numbers as shown in PowerPoint, 1-based)
Writes outdir/s<NN>_<shape name>.<ext> for every picture on those slides and prints its position on the
old slide (inches), which hints at how large it was shown.
"""
import io
import os
import re
import sys
import zipfile

from PIL import Image


def rels(z, path):
    xml = z.read(path).decode()
    return {re.search(r'Id="([^"]+)"', a).group(1): re.search(r'Target="([^"]+)"', a).group(1)
            for a in re.findall(r"<Relationship [^>]*/>", xml)}


def main(deck, outdir, slides):
    z = zipfile.ZipFile(deck)
    pres = z.read("ppt/presentation.xml").decode()
    prels = rels(z, "ppt/_rels/presentation.xml.rels")
    order = [prels[r] for r in re.findall(r'<p:sldId [^>]*r:id="(rId\d+)"', pres)]
    os.makedirs(outdir, exist_ok=True)
    for n in slides:
        name = order[n - 1].split("/")[-1]
        xml = z.read("ppt/slides/" + name).decode()
        srels = rels(z, f"ppt/slides/_rels/{name}.rels")
        for pic in re.findall(r"<p:pic>.*?</p:pic>", xml, re.S):
            shape = re.search(r'name="([^"]*)"', pic).group(1).replace(" ", "")
            target = srels[re.search(r'r:embed="([^"]+)"', pic).group(1)]
            part = "ppt/" + target[3:] if target.startswith("../") else "ppt/slides/" + target
            ext = os.path.splitext(target)[1].lower()
            data = z.read(part)
            out = os.path.join(outdir, f"s{n:02d}_{shape}{ext}")
            crop = re.search(r"<a:srcRect([^/]*)/>", pic)
            if crop and ext in (".png", ".jpg", ".jpeg", ".tif", ".tiff", ".gif"):
                d = {k: max(0, int(v)) / 1e5 for k, v in re.findall(r'(\w)="(-?\d+)"', crop.group(1))}
                im = Image.open(io.BytesIO(data))
                W, H = im.size
                im.crop((int(W * d.get("l", 0)), int(H * d.get("t", 0)),
                         int(W * (1 - d.get("r", 0))), int(H * (1 - d.get("b", 0))))).save(out)
            else:
                open(out, "wb").write(data)
            g = re.search(r'<a:off x="(\d+)" y="(\d+)"/><a:ext cx="(\d+)" cy="(\d+)"', pic)
            pos = [round(int(v) / 914400, 2) for v in g.groups()] if g else "?"
            print(out, "at (x, y, w, h) =", pos)


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2], [int(s) for s in sys.argv[3].split(",")])
