---
name: review_literature
family: literature
description: > LocalLiterature-only literature discovery, triage, deep-read, and comparison matrix. All operations go through D:/LocalLiterature SQLite database (library.db). Reads HTML/PDF from LocalLiterature. Imports new papers via LocalLiterature's import pipeline when local collection is insufficient. Sub-agents do deep-read + 5-dimension scoring per LocalLiterature's agent.md protocol. NOT for idea generation — use design_ideas. NOT for paper writing — use communicate.
---

# review_literature

**Core principle:** LocalLiterature-only. 所有文献操作必须通过 `D:/LocalLiterature` 进行。不自行搜索外部源。检索走 SQLite，精读走子 Agent + HTML，评分走 `agent_update.py`。

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

Before any search, verify LocalLiterature database and connectivity:

```bash
# LocalLiterature database check
ls "D:/LocalLiterature/library.db" 2>/dev/null && echo "DB_OK" || echo "DB_MISSING"
ls "D:/LocalLiterature/pdfs/" 2>/dev/null | wc -l && echo "PDFs in dir"
ls "D:/LocalLiterature/htmls/" 2>/dev/null | wc -l && echo "HTMLs in dir"

# Quick database query to verify it's readable
cd "D:/LocalLiterature" && python -c "
import sys; sys.path.insert(0, 'scripts')
from common import get_db
conn = get_db()
count = conn.execute('SELECT COUNT(*) FROM papers').fetchone()[0]
scored = conn.execute('SELECT COUNT(*) FROM papers WHERE score IS NOT NULL').fetchone()[0]
notes = conn.execute('SELECT COUNT(*) FROM notes').fetchone()[0]
print(f'Total papers: {count}, Scored: {scored}, Notes: {notes}')
conn.close()
"
```

If DB_MISSING → blocking_issue (no literature search possible).

**→ WRITE NOW: Create search-log.md immediately with pre-flight results. Do NOT wait.**
```bash
mkdir -p literature/paper-notes
```
Write `literature/search-log.md` NOW with a header row and pre-flight status:
```markdown
# Literature Search Log
## Pre-flight Status
- LocalLiterature DB: [OK/MISSING]
- Papers: [N total, M scored, K with notes]
- PDFs: [N files]
- HTMLs: [N files]
## Searches (append after each search)
| # | Method | Query | Results | Selected | Notes |
|---|--------|-------|---------|----------|-------|
```
Write this file BEFORE doing any searches.

### Step 1: Load Inputs

- project_context (research_question, constraints) from Phase 0
- If repair invocation: validation_feedback from prior failed self-validation

### Step 2: Search LocalLiterature (SQLite FTS + LIKE)

All searches go through `D:/LocalLiterature/library.db`. Use the `retrieve.py` API or direct SQL.

**Step 2a: FTS Full-Text Search**

```bash
cd "D:/LocalLiterature" && python -c "
import sys, json; sys.path.insert(0, 'scripts')
from retrieve import search_fts
results = search_fts('YOUR_QUERY_HERE', limit=20, min_score=0)
for p in results:
    score_str = f\"{p['score']:.1f}\" if p.get('score') else 'N/A'
    print(f\"[{score_str}] {p.get('arxiv_id', 'N/A')} ({p.get('year', '?')}) {p['title'][:80]}\")
"
```

Use at least 3 different keyword combinations derived from the RQ. For Chinese or complex queries, the `search_fts` function automatically falls back to `LIKE` pattern matching.

**Step 2b: Collection Filter**

If the project has a known collection tag:
```bash
cd "D:/LocalLiterature" && python -c "
import sys, json; sys.path.insert(0, 'scripts')
from retrieve import search_collection
results = search_collection('COLLECTION_NAME', limit=20, min_score=6.0)
for p in results:
    score_str = f\"{p['score']:.1f}\" if p.get('score') else 'N/A'
    print(f\"[{score_str}] {p.get('arxiv_id', 'N/A')} ({p.get('year', '?')}) {p['title'][:80]}\")
"
```

**Step 2c: Score-Threshold Browse**

```bash
cd "D:/LocalLiterature" && python -c "
import sys; sys.path.insert(0, 'scripts')
from common import get_db
conn = get_db()
c = conn.cursor()
c.execute('SELECT id, arxiv_id, title, authors, year, score, pdf_path FROM papers WHERE score >= ? ORDER BY score DESC NULLS LAST LIMIT 30', (6.0,))
for row in c.fetchall():
    print(f'[{row[\"score\"]:.1f}] {row[\"arxiv_id\"]} ({row[\"year\"]}) {row[\"title\"][:80]}')
conn.close()
"
```

**Step 2d: Direct SQL for Complex Queries**

```bash
cd "D:/LocalLiterature" && python -c "
import sys; sys.path.insert(0, 'scripts')
from common import get_db
conn = get_db()
c = conn.cursor()
# Example: search by keyword in title/abstract + year filter
c.execute('''
    SELECT id, arxiv_id, title, authors, year, score, pdf_path
    FROM papers
    WHERE (title LIKE ? OR abstract LIKE ?) AND year >= ?
    ORDER BY score DESC NULLS LAST
    LIMIT 30
''', ('%KEYWORD%', '%KEYWORD%', '2023'))
for row in c.fetchall():
    print(f'[{row[\"score\"]:.1f}] {row[\"arxiv_id\"]} ({row[\"year\"]}) {row[\"title\"][:80]}')
conn.close()
"
```

**Step 2e: Evaluate Results**

- If LocalLiterature returns >= 10 relevant papers → skip to Step 4 (Triage)
- If LocalLiterature returns < 10 relevant papers → proceed to Step 3 (Import to supplement)

### Step 3: Import New Papers (Only If Local Collection Insufficient)

**This is the ONLY way to add new papers.** Do NOT search external sources independently. Use LocalLiterature's `import_papers.py` which handles: arXiv API search → dedup → score_paper filter (>= 6.0) → download PDF → insert into library.db → rebuild FTS.

```bash
cd "D:/LocalLiterature" && python scripts/import_papers.py "YOUR_QUERY_HERE" 20 COLLECTION_NAME
```

This script:
1. Searches arXiv API via `search.py`
2. Deduplicates against existing papers in library.db
3. Scores candidates with `score_paper` (threshold >= 6.0)
4. Downloads PDFs to `pdfs/`
5. Inserts into `papers` table
6. Rebuilds FTS index

After import, re-run Step 2 searches to find the newly imported papers.

**If import fails (network down, rate-limited):** Use your KNOWLEDGE of known papers in the field — list by title, authors, year, venue, arXiv ID from memory. Mark all citations `_TODO_IMPORT_VERIFY_`. A literature review from domain knowledge with verification markers is better than an empty search log. When network is available later, run:
```bash
cd "D:/LocalLiterature" && python scripts/import_papers.py "QUERY" 20
```

### Step 4: Write Search Log

Write `literature/search-log.md`:
| # | Method | Query | Results | Selected | Notes |
|---|--------|-------|---------|----------|-------|

Record EVERY search attempt, including failed ones.
If total unique candidates < 20 → expand search terms, re-run from Step 2.

→ CHECKPOINT: Write search-log.md NOW. Verify: `ls literature/search-log.md`. Then continue.

### Step 5: Triage Papers

For each candidate from the SQLite search results:
1. Read abstract from the database (already available from the `papers` table)
2. Check if analysis/study notes already exist in the `notes` table:
```bash
cd "D:/LocalLiterature" && python -c "
import sys; sys.path.insert(0, 'scripts')
from common import get_db
conn = get_db()
c = conn.cursor()
c.execute('SELECT p.id, p.arxiv_id, p.title, p.score, n.note_type, LENGTH(n.content) as note_len FROM papers p LEFT JOIN notes n ON n.paper_id = p.id WHERE p.id = ?', (PAPER_ID,))
for row in c.fetchall():
    print(f'ID={row[0]} {row[1]} score={row[3]} note[{row[4]}]={row[5]} chars')
conn.close()
"
```
3. Write 1-2 sentence triage rationale: why include or exclude
4. Select >= 5 papers for deep-read based on relevance and diversity

Papers that already have analysis notes in the database can be used directly — their notes are already curated. Prioritize papers with existing analysis for efficiency.

### Step 6: Deep-Read Selected Papers via Sub-Agents

**CRITICAL: Per LocalLiterature's agent.md, deep-read + scoring MUST be done by spawning sub-Agents.** Do NOT read full paper text in the main context and score yourself. Each paper gets its own sub-Agent.

For each selected paper:

**Step 6a: Check if paper already has analysis + study notes**
```bash
cd "D:/LocalLiterature" && python -c "
import sys; sys.path.insert(0, 'scripts')
from common import get_db
conn = get_db()
c = conn.cursor()
c.execute(\"SELECT note_type, LENGTH(content) FROM notes WHERE paper_id = ?\", (PAPER_ID,))
for row in c.fetchall():
    print(f'{row[0]}: {row[1]} chars')
conn.close()
"
```

If BOTH analysis and study notes exist → skip to writing `literature/paper-notes/<id>-note.md` from the existing notes. No need to re-analyze.

**Step 6b: Spawn sub-Agent for papers missing analysis**

Per LocalLiterature's agent.md protocol, spawn a sub-Agent for each paper that needs analysis:

```
Agent(prompt="""
You are a LocalLiterature analysis sub-Agent. Analyze paper ID={PAPER_ID}.

Steps:
1. Read the paper's HTML file from D:/LocalLiterature/htmls/{arxiv_id}.html (use Read tool)
   - If HTML unavailable or too short, read PDF from D:/LocalLiterature/pdfs/{arxiv_id}.pdf
   - If both unavailable, use arXiv MCP as last resort: mcp__arxiv__arxiv_read_paper(paper_id="{arxiv_id}")
2. Write analysis report following templates/analysis_template.md (Chinese Markdown)
3. Write study note following templates/study_note_template.md (Chinese Markdown)
4. Include the 5-dimension scoring table (0-10 scale):
   | 维度 | 分数 | 依据 |
   |------|------|------|
   | 问题重要性 | X/10 | ... |
   | 方法新颖性 | X/10 | ... |
   | 理论严谨性 | X/10 | ... |
   | 实验充分性 | X/10 | ... |
   | 实用可部署性 | X/10 | ... |
   Do NOT calculate the total — agent_update.py will auto-calculate.
5. Write tmp_result_{PAPER_ID}.json with {"analysis": "...", "study_note": "..."}
6. Run: cd D:/LocalLiterature && python scripts/agent_update.py {PAPER_ID} --file tmp_result_{PAPER_ID}.json
7. Delete the temporary JSON file

Paper metadata:
- Title: {title}
- Authors: {authors}
- Year: {year}
- arXiv ID: {arxiv_id}
- PDF: D:/LocalLiterature/pdfs/{arxiv_id}.pdf
- HTML: D:/LocalLiterature/htmls/{arxiv_id}.html

All output must be in Chinese (中文). Score based on actual paper content, never guess.
""")
```

**Step 6c: Write paper notes to literature/ output**

After each paper (whether newly analyzed or using existing notes), write structured notes to `literature/paper-notes/<id>-note.md`:

```markdown
# {Title}

**Citation:** Authors (Year). Venue.
**arXiv ID:** {arxiv_id}
**LocalLiterature Score:** {score}/10
**LocalLiterature Path:** D:/LocalLiterature/pdfs/{arxiv_id}.pdf

## Summary
[From analysis note — 问题与定位 section]

## Method
[From analysis note — 方法评估 section]

## Key Results
[From analysis note — 实验评估 section]

## Scoring
| 维度 | 分数 | 依据 |
|------|------|------|
| 问题重要性 | X/10 | ... |
| 方法新颖性 | X/10 | ... |
| 理论严谨性 | X/10 | ... |
| 实验充分性 | X/10 | ... |
| 实用可部署性 | X/10 | ... |

## Limitations
[From analysis note — 关键风险提示 section]

## Relevance to RQ
[0-10, with justification — written by main agent based on project RQ]

## Use As
[baseline | inspiration | contrast | citation-only]
```

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
- [ ] LocalLiterature SQLite searched (FTS + LIKE + collection)?
- [ ] If insufficient, import_papers.py used to supplement?
- [ ] Total candidates >= 20?
- [ ] Each candidate has triage rationale?
- [ ] Deep-read papers >= 5?
- [ ] Deep-read done via sub-Agents (not in main context)?
- [ ] Sub-Agent results written back to library.db via agent_update.py?
- [ ] Each deep-read paper has complete structured notes in literature/paper-notes/?
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

## Key Rules (LocalLiterature-specific)

1. **All searches through SQLite** — never search arXiv/paperplain/crossref/DBLP directly. Use `D:/LocalLiterature/library.db` via `retrieve.py` or direct SQL.
2. **New papers only via import_papers.py** — this handles arXiv API search, dedup, scoring, PDF download, and database insertion.
3. **Deep-read via sub-Agents** — per LocalLiterature's agent.md, each paper must be analyzed by a separate sub-Agent that reads HTML/PDF, writes analysis + study notes, and updates library.db via `agent_update.py`.
4. **Read HTML first** — sub-Agents must try `htmls/{arxiv_id}.html` before PDF or arXiv MCP.
5. **5-dimension scoring** — use LocalLiterature's scoring dimensions (问题重要性/方法新颖性/理论严谨性/实验充分性/实用可部署性), NOT the old 9-column evidence strength.
6. **All notes in Chinese** — per LocalLiterature's convention, analysis reports and study notes must be in 中文.
7. **Reuse existing notes** — if a paper already has analysis + study notes in the `notes` table, extract from there instead of re-analyzing.
8. **Score auto-calculation** — sub-Agents must NOT calculate the total score. `agent_update.py` auto-extracts 5 dimension scores and computes the weighted total.

## Output

- `literature/search-log.md` — all searches (including failed)
- `literature/paper-notes/` — one .md per deep-read paper
- `literature/comparison-matrix.md` — 9-column matrix
- `literature/gap-analysis.md` — research gap statement

## Next Skill

After this skill: `seek:design_ideas`
