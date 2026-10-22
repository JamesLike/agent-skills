#!/usr/bin/env python3

import requests
import sys
import json
import yaml

CONFIG_PATH = "../config.yaml"

def load_config():
    with open(CONFIG_PATH, "r") as f:
        return yaml.safe_load(f)

def create_zotero_item(metadata, config):
    url = f"https://api.zotero.org/{config['zotero']['library_type']}s/{config['zotero']['library_id']}/items"

    headers = {
        "Zotero-API-Key": config["zotero"]["api_key"],
        "Content-Type": "application/json"
    }

    item = {
        "itemType": "journalArticle",
        "title": metadata["title"],
        "creators": [
            {
                "creatorType": "author",
                "name": author
            } for author in metadata["authors"]
        ],
        "publicationTitle": metadata["journal"],
        "date": str(metadata["year"]),
        "volume": metadata["volume"],
        "pages": metadata["pages"],
        "DOI": metadata["doi"]
    }

    r = requests.post(url, headers=headers, data=json.dumps([item]))

    if r.status_code in [200, 201]:
        print("SUCCESS: Added to Zotero")
    else:
        print("ERROR:", r.text)

def main():
    if len(sys.argv) < 2:
        print("Usage: add_to_zotero.py <metadata_json>")
        sys.exit(1)

    metadata = json.loads(sys.argv[1])
    config = load_config()

    create_zotero_item(metadata, config)

if __name__ == "__main__":
    main()
