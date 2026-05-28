# Literature Review Standards

> Violating any hard rule → literature review is incomplete; cannot proceed to idea design.

## Hard Rules

### Coverage
- [ ] LocalLiterature (D:/LocalLiterature/library.db) searched via `retrieve.py` or direct SQL (FTS + LIKE + collection + score-threshold)
- [ ] Search performed with >= 3 different keyword combinations
- [ ] If local collection < 10 relevant papers, `import_papers.py` used to supplement
- [ ] Total search results ≥ 20 candidate papers

### Triage
- [ ] Each candidate paper has a 1-2 sentence triage rationale (why included / why excluded)
- [ ] Deep-read papers ≥ 5
- [ ] Selected papers have complete metadata (author, title, year, venue/journal, DOI/arXiv ID)

### Analysis
- [ ] Each deep-read paper has structured notes:
  - Research Question
  - Method
  - Data
  - Main Claim
  - Evidence Strength
  - Limitations
  - Relevance to this project (0-10)
  - Use As: baseline | inspiration | contrast | citation-only
- [ ] Comparison matrix ≥ 5 rows × 9 columns (Citation | Question | Method | Data | Main Claim | Evidence | Limitation | Relevance | Use As)
- [ ] Research gap stated clearly in ≤ 3 sentences:
  - "Existing work has done [X]"
  - "But [Y] has not been addressed/verified"
  - "This project's positioning is [Z]"
