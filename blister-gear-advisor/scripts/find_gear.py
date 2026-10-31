#!/usr/bin/env python3
"""Search the Blister guide notes (and optionally full text) for products or terms.

Each hit is printed with its guide year and the section it falls under, so you can
see at a glance which class a ski was reviewed in each season.

Usage:
  python3 -I find_gear.py "Mindbender 99" ["Enforcer 100" ...]   # notes, all years
  python3 -I find_gear.py --full "Mindbender 99"                 # also search full text
  python3 -I find_gear.py --year 2026-2027 "Canvas"              # one guide only
  python3 -I find_gear.py --sections 2026-2027                   # list a guide's sections

Terms are case-insensitive substrings; several terms are OR-ed together.
"""
import argparse
import re
from pathlib import Path

REFS = Path(__file__).resolve().parent.parent / "references"
YEARS = sorted(f.stem for f in (REFS / "notes").glob("20??-20??.md"))


def search(path, patterns, max_len, with_sections):
    section = ""
    hits = []
    for n, line in enumerate(path.read_text(errors="replace").splitlines(), 1):
        if with_sections and line.startswith("#"):
            section = line.lstrip("#").strip()
        if any(p.search(line) for p in patterns):
            text = line.strip()
            if len(text) > max_len:
                text = text[:max_len] + " …"
            hits.append((n, section, text))
    return hits


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("terms", nargs="*")
    ap.add_argument("--full", action="store_true", help="also search full guide text")
    ap.add_argument("--year", choices=YEARS, help="restrict to one guide")
    ap.add_argument("--sections", choices=YEARS, help="list section headings of a guide's notes")
    ap.add_argument("--max-len", type=int, default=700, help="truncate long lines")
    args = ap.parse_args()

    if args.sections:
        # Notes line numbers, for `sed -n`; any [L...] inside a heading is a full-text line.
        for n, line in enumerate((REFS / "notes" / f"{args.sections}.md").read_text().splitlines(), 1):
            if line.startswith("#"):
                print(f"{n:5d}  {line}")
        return
    if not args.terms:
        ap.error("give at least one search term")

    patterns = [re.compile(re.escape(t), re.I) for t in args.terms]
    years = [args.year] if args.year else YEARS
    for y in years:
        hits = search(REFS / "notes" / f"{y}.md", patterns, args.max_len, True)
        print(f"===== {y} notes: {len(hits)} hit(s)")
        for n, sec, text in hits:
            print(f"[L{n} | {sec}] {text}")
        full = REFS / "fulltext" / f"{y}.txt"
        if args.full and not full.exists():
            print(f"----- {y} full text: not available")
        elif args.full:
            hits = search(full, patterns, 300, False)
            print(f"----- {y} full text: {len(hits)} hit(s)")
            for n, _, text in hits:
                print(f"[L{n}] {text}")


if __name__ == "__main__":
    main()
