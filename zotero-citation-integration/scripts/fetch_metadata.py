#!/usr/bin/env python3

import requests
import sys

def fetch_crossref(doi):
    url = f"https://api.crossref.org/works/{doi}"
    r = requests.get(url)
    if r.status_code != 200:
        return None
    data = r.json()["message"]

    return {
        "title": data.get("title", [""])[0],
        "authors": [
            f"{a.get('family', '')}, {a.get('given', '')}"
            for a in data.get("author", [])
        ],
        "journal": data.get("container-title", [""])[0],
        "year": data.get("issued", {}).get("date-parts", [[None]])[0][0],
        "volume": data.get("volume"),
        "pages": data.get("page"),
        "doi": doi
    }

def main():
    if len(sys.argv) < 2:
        print("Usage: fetch_metadata.py DOI")
        sys.exit(1)

    doi = sys.argv[1]
    metadata = fetch_crossref(doi)

    if metadata:
        print(metadata)
    else:
        print("ERROR: Could not fetch metadata")

if __name__ == "__main__":
    main()
