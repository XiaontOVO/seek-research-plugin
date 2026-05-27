---
name: review_literature
family: literature
description: > Zotero-first literature discovery, triage, deep-read, and comparison matrix. Queries Zotero local/Web API first, then arXiv MCP + paperplain MCP with 5-tier curl fallback chain. New papers imported to Zotero immediately. NOT for idea generation — use design_ideas. NOT for paper writing — use communicate.
---

# review_literature

**Core principle:** Zotero-first. Triage before download. No paper enters deep-read without a triage rationale. All potentially useful papers go to Zotero first.

Zotero-first literature review engine. Searches the existing Zotero library for relevant papers. If not enough, searches external sources (arXiv MCP → paperplain MCP → arXiv curl → CrossRef curl → DBLP curl) and adds new papers to Zotero immediately. Then deep-reads selected papers and builds a 9-column comparison matrix to identify the research gap.

## When To Use

Trigger phrases:
- "Search for papers on [topic]" / "search literature on [topic]"
- "Find related work for [research question]"
- "What's the state of the art in [field]?"
- "Build literature review" / "do literature survey"
- Invoked by orchestrator after Phase 0 (define_context) completes.

## NOT For

- Generating research ideas from literature gaps — use `seek:design_ideas`
- Writing the related work section of a paper — use `seek:communicate`
- Single paper deep analysis only — this skill does batch review
- Checking novelty of a specific idea — that's part of `seek:design_ideas`

## Standards

Before any action, load `references/standards/literature-standards.md`. Every checklist item is a hard constraint.

## Output Directory Convention

All paths from `references/paths.yml`. Before any work, create the output directory:

```bash
mkdir -p literature/paper-notes
```

All output files go under `literature/`. Never scatter files elsewhere.

## Resume Support

This skill supports resumption. Before starting, check which output files already exist:
```bash
ls literature/search-log.md 2>/dev/null && echo "SEARCH_DONE" || echo "SEARCH_NEEDED"
ls literature/comparison-matrix.md 2>/dev/null && echo "MATRIX_DONE" || echo "MATRIX_NEEDED"
ls literature/gap-analysis.md 2>/dev/null && echo "GAP_DONE" || echo "GAP_NEEDED"
```
Skip any step whose output file already exists. Pick up from the first missing file.

CRITICAL: After EVERY step below, write the output file to disk IMMEDIATELY. Do NOT batch writes. Each step = one file on disk = one checkpoint. If you get interrupted, the next invocation resumes from the first missing file.

## Workflow

### Step 0: Pre-Flight Checks
Before any search, verify connectivity and permissions:
```bash
# Zotero connectivity (if configured)
curl -s --max-time 2 "http://localhost:23119/api/users/0/items?limit=1" -H "Zotero-Allowed-Request: true" 2>/dev/null && echo "ZOTERO_LOCAL_OK" || echo "ZOTERO_LOCAL_UNAVAILABLE"
# arXiv connectivity
curl -s --connect-timeout 5 "https://export.arxiv.org/api/query?search_query=all:test&max_results=1" 2>/dev/null | grep -q "<id>" && echo "ARXIV_OK" || echo "ARXIV_DOWN"
# MCP availability
echo "MCP tools: arxiv_search=$(type mcp__arxiv__arxiv_search 2>/dev/null && echo yes || echo no)"
```
Record which sources are available. If ALL fail → blocking_issue (no search possible). If some fail → non_blocking_warning, proceed with available sources.

**→ WRITE NOW: Create search-log.md immediately with pre-flight results. Do NOT wait.**
```bash
mkdir -p literature/paper-notes
```
Write `literature/search-log.md` NOW with a header row and pre-flight status:
```markdown
# Literature Search Log
## Pre-flight Status
- Zotero: [AVAILABLE/UNAVAILABLE]
- arXiv: [OK/DOWN]
- MCP: [AVAILABLE/UNAVAILABLE]
## Searches (append after each search)
| # | Source | Query | Results | Selected | Notes |
|---|--------|-------|---------|----------|-------|
```
Write this file BEFORE doing any searches. Append one row after each search attempt. Never wait until all searches are done.

### Step 1: Load Inputs
- project_context (research_question, zotero_status, constraints) from Phase 0
- If repair invocation: validation_feedback from prior failed self-validation

### Step 2: Search Zotero Library (Zotero-first — ported from AutoResearch literature-zotero)

**Step 2a: Pre-Flight Permission Check**

Before any Zotero API call, verify the API key exists and has correct permissions:
```python
import json, os, urllib.request

cfg_path = os.path.expanduser("~/.zotero/config.json")
if not os.path.exists(cfg_path):
    print("ZOTERO_CONFIG_MISSING: ~/.zotero/config.json not found")
    # Zotero not configured — record as non_blocking_warning, skip to Step 3 (external search)
else:
    with open(cfg_path) as f:
        cfg = json.load(f)
    API_KEY = cfg["api_key"]
    resp = urllib.request.urlopen(
        urllib.request.Request("https://api.zotero.org/keys/" + API_KEY,
            headers={"Zotero-API-Key": API_KEY})
    )
    key_info = json.loads(resp.read())
    has_write = key_info.get("access", {}).get("user", {}).get("write", False)
    USER_ID = cfg["user_id"]
    print(f"Zotero: user={USER_ID}, write={has_write}")
```
Decision tree:
- config missing → non_blocking_warning, skip to external search
- key invalid (401/403) → non_blocking_warning, skip to external search
- key valid, no write → WARN (can read but not import new papers)
- key valid, read+write → PASS

**Step 2b: Search via Zotero Local API (read-only, requires Zotero desktop running)**

Try local API first (fast, no rate limit):
```bash
curl -s --max-time 3 "http://localhost:23119/api/users/0/items?q=<URL_ENCODED_KEYWORDS>&limit=50" -H "Zotero-Allowed-Request: true"
```
Parse the JSON response. Each item has: `data.title`, `data.creators`, `data.date`, `data.DOI`, `data.url`, `data.extra` (contains arXiv ID), `data.abstractNote`, `data.tags`, `data.collections`.

**Step 2c: Search via Zotero Web API (read+write, works even without desktop)**

If local API unavailable or returns < 10 results, search via Web API:
```python
import urllib.request, json
url = f"https://api.zotero.org/users/{USER_ID}/items?q=<URL_ENCODED_KEYWORDS>&limit=100"
req = urllib.request.Request(url, headers={"Zotero-API-Key": API_KEY})
resp = urllib.request.urlopen(req, timeout=10)
items = json.loads(resp.read())
```

**Step 2d: Score and Select**

Score each paper by relevance to the RQ (match in title/abstract). Keep papers with score >= 3/5.
If Zotero returns >= 10 relevant papers → skip external search entirely. Zotero is sufficient.
If Zotero returns < 10 papers → proceed to Step 3 (external search) to supplement.
If Zotero unavailable entirely → record as non_blocking_warning, proceed to Step 3.

### Step 3: External Search (Five-Tier Fallback)

Use at least 3 different keyword combinations derived from the RQ. If one tier fails (429, empty, error), automatically try the next.

**Tier 1 — arXiv MCP:**
```
mcp__arxiv__arxiv_search(query="<keywords>", max_results=20, sort_by="relevance")
mcp__arxiv__arxiv_search(query="<alternative keywords>", max_results=20, sort_by="submitted")
```

**Tier 2 — paperplain MCP:**
```
mcp__paperplain__search_research(query="<keywords>", max_results=15)
```

**Tier 3 — arXiv curl REST API:**
Use `+AND+` between terms — spaces become OR, which returns noise.
```bash
curl -s "https://export.arxiv.org/api/query?search_query=all:<TERM1>+AND+all:<TERM2>&start=0&max_results=20&sortBy=relevance"
```
Parse XML: `<entry>` → `<id>`, `<title>`, `<summary>`, `<author>`, `<published>`.
If no results, simplify to fewer AND terms.

**Tier 4 — CrossRef curl REST API:**
```bash
curl -s "https://api.crossref.org/works?query=<KEYWORDS>&rows=20&filter=type:journal-article"
```

**Tier 5 — DBLP curl REST API:**
```bash
curl -s "https://dblp.org/search/publ/api?q=<KEYWORDS>&format=json&h=20"
```

**After each successful external search:** Import new papers to Zotero:
```python
import json, urllib.request, time
# POST https://api.zotero.org/users/{user_id}/items
# Headers: Zotero-API-Key, Content-Type: application/json
# Body: {itemType, title, creators, DOI, url, extra, abstractNote}
# time.sleep(0.3) between POSTs
```

Or use the bundled script:
```bash
python d:/Research/plugin/seek/scripts/zotero_batch_import.py --source results.json --collection "Seek-Research"
```

**Deduplicate** by arXiv ID (from `extra` field) or DOI across all sources.

**If ALL tiers fail** (rate-limited + network down): STOP trying after 3 attempts per tier. Use your KNOWLEDGE of known papers in the field — list by title, authors, year, venue, arXiv ID from memory. Mark all citations `_TODO_API_VERIFY_`. A literature review from domain knowledge with verification markers is better than an empty search log. Proceed immediately to paper notes and comparison matrix.

### Step 4: Write Search Log

Write `literature/search-log.md`:
| # | Source | Query | Results | Selected | Notes |

Record EVERY search attempt, including rate-limited/failed ones.
If total unique candidates < 20 → expand search terms, re-run from Tier 1.

→ CHECKPOINT: Write search-log.md NOW. Verify: `ls literature/search-log.md`. Then continue.

### Step 5: Triage Papers

For each candidate:
1. Read abstract via MCP: `mcp__arxiv__arxiv_read_paper(paper_id="ID", max_characters=2000)` or curl: `curl -s "https://export.arxiv.org/api/query?id_list=ID"` (parse `<summary>` tag)
2. Write 1-2 sentence triage rationale: why include or exclude
3. Select >= 5 papers for deep-read based on relevance and diversity

Triage-before-download: do NOT download PDFs at this stage. MCP/curl abstract reading is sufficient.

### Step 6: Deep-Read Selected Papers

For each selected paper:
1. Read full text: `mcp__arxiv__arxiv_read_paper(paper_id="ID")` (HTML render). If HTML unavailable, note PDF URL for later retrieval.
2. Read only: abstract, introduction, method, key results, conclusion. Skip appendices.
3. Write structured notes to `literature/paper-notes/<id>-note.md`:
   - **Citation:** Authors (Year). Venue.
   - **Research Question:** [1 sentence]
   - **Method:** [Concrete details — what they actually did]
   - **Data:** [What they tested on]
   - **Main Claim:** [Their core contribution]
   - **Evidence Strength:** [0-10, with justification]
   - **Limitations:** [Their own + your assessment]
   - **Relevance:** [0-10 to your RQ]
   - **Use As:** [baseline | inspiration | contrast | citation-only]

→ CHECKPOINT: Write THIS paper note to disk NOW before reading the next paper. Verify: `ls literature/paper-notes/`.

### Step 7: Build Comparison Matrix

9-column table with all deep-read papers (>= 5 rows):

| Citation | Question | Method | Data | Main Claim | Evidence | Limitation | Relevance | Use As |

Each row = one paper. Each cell = 1-2 sentences. Fill unknowns with `?` (note: "incomplete — run deeper analysis").

→ CHECKPOINT: Write comparison-matrix.md NOW. Verify: `ls literature/comparison-matrix.md`. Then continue.

### Step 8: Identify Research Gap

State in <= 3 sentences:
1. "Existing work has done [X]"
2. "But [Y] has not been addressed/verified"
3. "This project's positioning is [Z]"

Write to `literature/gap-analysis.md`.

→ CHECKPOINT: Write gap-analysis.md NOW. Verify: `ls literature/gap-analysis.md`. Then continue to self-validate.

### Step 9: Self-Validate

Load `references/standards/literature-standards.md`. Check EVERY item against produced output:
- [ ] Zotero searched (if available)?
- [ ] External search attempted >= 3 keyword combinations across all viable tiers?
- [ ] Total candidates >= 20?
- [ ] Each candidate has triage rationale?
- [ ] Deep-read papers >= 5?
- [ ] Each deep-read paper has complete structured notes?
- [ ] Comparison matrix >= 5 rows x 9 columns?
- [ ] Research gap stated in <= 3 sentences?

Unchecked items → blocking_issues. Edge cases → non_blocking_warnings.
Non-goal compliance:
- [ ] Search scope does not expand into areas listed as non_goals?
- [ ] Selected papers are relevant to the RQ?

Return valid: true only if ALL coverage + analysis items pass AND all output files exist on disk AND non-goal compliant.
Before returning valid=true, verify with:
```bash
ls literature/search-log.md literature/comparison-matrix.md literature/gap-analysis.md 2>/dev/null || echo "MISSING_FILES"
```
Missing output files → blocking_issue. Do NOT mark valid=true with missing files.

### Step 10: Update State

Update `guidetree/project.yaml`:
- phases.literature.status = "done"
- phases.literature.valid = (true/false)
- phases.literature.artifacts = { search_log, paper_notes, comparison_matrix, gap_analysis }
- If valid: set current_phase = "ideas"

## Output

- `literature/search-log.md` — all searches (including failed)
- `literature/paper-notes/` — one .md per deep-read paper
- `literature/comparison-matrix.md` — 9-column matrix
- `literature/gap-analysis.md` — research gap statement

## Next Skill

After this skill: `seek:design_ideas`
