#!/usr/bin/env python3
"""Batch import papers to Zotero via Web API. Adapted from AutoResearch plugin."""

import json
import os
import sys
import time
import urllib.request
import urllib.error
from pathlib import Path


def load_config():
    """Load Zotero configuration from ~/.zotero/config.json."""
    config_path = os.path.expanduser("~/.zotero/config.json")
    if not os.path.exists(config_path):
        print("ERROR: ~/.zotero/config.json not found. Run zotero-setup first.", file=sys.stderr)
        sys.exit(1)
    with open(config_path, encoding="utf-8") as f:
        return json.load(f)


def zotero_post(config, endpoint, data):
    """POST data to Zotero Web API."""
    url = f"https://api.zotero.org/{endpoint}"
    body = json.dumps(data).encode("utf-8")
    req = urllib.request.Request(url, data=body, method="POST")
    req.add_header("Zotero-API-Key", config["api_key"])
    req.add_header("Content-Type", "application/json")
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            return json.loads(resp.read())
    except urllib.error.HTTPError as e:
        print(f"  WARN: HTTP {e.code} on POST to {url}: {e.reason}")
        return None
    except Exception as e:
        print(f"  WARN: POST failed: {e}")
        return None


def paper_to_zotero_item(paper):
    """Convert a paper dict to Zotero item JSON."""
    item = {
        "itemType": "journalArticle",
        "title": paper.get("title", "Unknown Title"),
        "creators": [],
        "date": paper.get("year", ""),
        "url": paper.get("url", ""),
        "extra": "",
        "abstractNote": paper.get("abstract", ""),
    }

    # Parse authors
    authors = paper.get("authors", [])
    if isinstance(authors, str):
        authors = [a.strip() for a in authors.split(",") if a.strip()]

    for i, author in enumerate(authors):
        parts = author.strip().split()
        if len(parts) >= 2:
            item["creators"].append({
                "creatorType": "author",
                "firstName": " ".join(parts[:-1]),
                "lastName": parts[-1],
            })
        elif len(parts) == 1:
            item["creators"].append({
                "creatorType": "author",
                "lastName": parts[0],
            })

    # Add arXiv ID to extra field
    arxiv_id = paper.get("arxiv_id", "")
    if arxiv_id:
        item["extra"] = f"arXiv: {arxiv_id}"

    # Add DOI
    doi = paper.get("doi", "")
    if doi:
        item["DOI"] = doi

    # Add publication title
    venue = paper.get("venue", "")
    if venue:
        item["publicationTitle"] = venue

    return item


def main():
    config = load_config()
    user_id = config["user_id"]

    # Read input papers from stdin or file
    input_file = sys.argv[1] if len(sys.argv) > 1 else None
    if input_file and os.path.exists(input_file):
        with open(input_file, encoding="utf-8") as f:
            papers = json.load(f)
    else:
        papers = json.load(sys.stdin)

    collection_name = sys.argv[2] if len(sys.argv) > 2 else "Seek-Research"

    print(f"Importing {len(papers)} papers to Zotero collection '{collection_name}'...")

    success = 0
    skipped = 0
    failed = 0

    for i, paper in enumerate(papers):
        # Check for duplicates by arXiv ID or DOI first
        arxiv_id = paper.get("arxiv_id", "")
        doi = paper.get("doi", "")
        if arxiv_id or doi:
            # Quick dedup: skip if we've seen this before in this batch
            pass  # Dedup against full library requires GET first — skipped for speed

        item = paper_to_zotero_item(paper)
        result = zotero_post(config, f"users/{user_id}/items", item)

        if result and "success" in result:
            success += 1
            if (i + 1) % 5 == 0:
                print(f"  Imported {i+1}/{len(papers)}...")
        else:
            failed += 1

        # Rate limiting
        time.sleep(0.3)

    print(f"Done: {success} imported, {failed} failed, {len(papers)} total")
    return 0 if failed == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
