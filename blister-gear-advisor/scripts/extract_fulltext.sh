#!/bin/bash
# Regenerate references/fulltext/<year>.txt from the Blister guide PDFs.
# Usage: extract_fulltext.sh [pdf_dir]   (default: ~/Downloads/blister)
# Needs Ghostscript (gs). Two-column pages come out interleaved line by line.
set -euo pipefail
PDF_DIR="${1:-$HOME/Downloads/blister}"
OUT="$(cd "$(dirname "$0")/.." && pwd)/references/fulltext"
mkdir -p "$OUT"
for f in "$PDF_DIR"/*.pdf; do
  y=$(basename "$f" | grep -oE '20[0-9]{2}-(20)?[0-9]{2}' | head -1 | sed -E 's/^(20([0-9]{2}))-([0-9]{2})$/\1-20\3/') || continue; [ -n "$y" ] || continue
  tmp=$(mktemp)
  gs -q -dNOPAUSE -dBATCH -dSAFER -sDEVICE=txtwrite -o "$tmp" "$f"
  tr -s ' \t' ' ' < "$tmp" | sed 's/^ //' | grep -v '^\s*$' > "$OUT/$y.txt"
  rm -f "$tmp"
  echo "wrote $OUT/$y.txt"
done
