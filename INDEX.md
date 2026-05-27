# Seek Plugin — Skill Index

## Master Index

| # | Skill | Family | Description |
|---|-------|--------|-------------|
| 1 | `seek:orchestrate` | orchestration | State machine: inspect pipeline state, select next skill, enforce validation gates |
| 2 | `seek:define_context` | context | Phase 0 — Research framing: Socratic interview, hardware detection, Zotero check |
| 3 | `seek:review_literature` | literature | Phase 1 — Zotero-first discovery, 5-tier fallback, triage, deep-read, comparison matrix |
| 4 | `seek:discover_ideas` | ideas | Phase 2a — Divergent: brainstorm 8-12 ideas from gaps, filter, pilot top 2-3 |
| 5 | `seek:design_ideas` | ideas | Phase 2b — Convergent: Socratic design, Claims DAG, Matrix v1, novelty gate, roadmap |
| 6 | `seek:investigate` | investigation | Phase 3 — Claims-driven unified code+experiment loop |
| 7 | `seek:communicate` | communication | Phase 4 — Claims Matrix → paper plan → write → Agent review |
| 8 | `seek:audit` | audit | Phase 5 — 3-Agent gate audit + claims + citations + reproducibility + Gold scoring |
| 9 | `seek:crystallize` | meta | Post-pipeline — Gold mining: extract, score, evidence folder, vulnerability map |

## Standards (7 files)

| # | Standard | Applies To |
|---|----------|-----------|
| 1 | `context-standards.md` | define_context |
| 2 | `literature-standards.md` | review_literature |
| 3 | `idea-standards.md` | discover_ideas, design_ideas |
| 4 | `coding-standards.md` | investigate (code) |
| 5 | `experiment-standards.md` | investigate (experiments) |
| 6 | `writing-standards.md` | communicate |
| 7 | `audit-standards.md` | audit |

## Templates

| # | Template | Used By |
|---|----------|---------|
| 1 | `code-review-checklist.md` | investigate (code review step) |
| 2 | `claims-audit-checklist.md` | audit (claims verification) |
| 3 | `domains/computational-experiment/` | Phase planning reference |
| 4 | `domains/literature-survey/` | Phase planning reference |

## Pipeline Order

```
define_context → review_literature → discover_ideas → design_ideas → investigate → communicate → audit → crystallize
```

## Repair Strategy

No separate repair skills. Validation failure → re-invoke same skill with feedback. Max 3 attempts.
