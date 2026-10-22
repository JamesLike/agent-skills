---
name: zotero-citation-integration
description: "Citation management via a Zotero library: look up a DOI/PMID/arXiv ID/title in Zotero, format it in JACS style (inline, bibliography, or BibTeX), and if missing, fetch metadata and add it to Zotero. Requires a config.yaml with Zotero API key and library ID."
argument-hint: <DOI, PMID, arXiv ID, or title>
---

# Zotero Citation Integration Skill

## Purpose
This skill provides seamless citation management and formatting using a Zotero library. It prioritizes retrieving citations from the user's Zotero database and formats them in JACS style. If a citation is not found locally, the skill automatically retrieves metadata from external databases, adds it to Zotero, and returns a properly formatted citation.

## Core Capabilities

1. Search Zotero library using API
2. Format citations in JACS style (default)
3. Automatically retrieve missing citations using DOI, title, or PubMed queries
4. Add missing entries to Zotero library
5. Return formatted inline and bibliography-ready citations

---

## Inputs

- DOI, PMID, arXiv ID, or title string
- Optional: citation style (default = JACS)
- Optional: output format
  - inline
  - bibliography
  - bibtex

---

## Outputs

- Formatted citation (JACS)
- Zotero item key
- BibTeX entry (optional)
- Confirmation if item was added to Zotero

---

## Workflow

1. **Query Zotero API**
   - Use local API key and library ID from config.yaml
   - Search by DOI or title

2. **If found**
   - Retrieve metadata
   - Format using CSL (JACS)

3. **If not found**
   - Call `scripts/fetch_metadata.py`
   - Resolve metadata via CrossRef / PubMed / OpenAlex
   - Validate metadata fields

4. **Add to Zotero**
   - Call `scripts/add_to_zotero.py`
   - Push formatted JSON payload to Zotero API

5. **Format citation**
   - Apply JACS CSL template
   - Return formatted output

---

## Configuration

See `config.yaml` for:
- Zotero API key
- Library ID
- Default citation style
- External API preferences

---

## Constraints

- Always prefer Zotero entries over external sources
- Never duplicate entries (check DOI match first)
- Ensure required fields for JACS formatting:
  - authors
  - title
  - journal
  - year
  - volume
  - pages

---

## Error Handling

- If metadata incomplete → attempt secondary source
- If Zotero API fails → retry once, then return warning
- If DOI invalid → fallback to title search

---

## Example Usage

Input:
"10.1021/jacs.0c12345"

Output:
Smith, J.; Doe, A. J. Am. Chem. Soc. 2020, 142, 1234–1245.

---

## Notes for Agent

- This skill is stateful with respect to the Zotero library
- Maintain consistency in citation formatting across outputs
- Cache recent queries to reduce API calls
