# Seek — Foolproof Research Pipeline

A Claude Code plugin that guides research from question to paper through a fixed 6-phase pipeline with mandatory standards and validation gates at every level.

**Design philosophy:** Before any action, there must be explicit standards. Big goals must be decomposed. Plans must be detailed enough that anyone can execute them. Execution must be checked against standards.

## Quick Start

```
/seeker
```

The orchestrator inspects the project state and tells you exactly what to do next. You cannot get lost.

## Pipeline

```
Context → Literature → Ideas → Investigation → Communication → Audit
```

## The Core Innovation: Claims-Driven Investigation

Unlike traditional pipelines that separate "coding" and "experimenting" into sequential phases, Seek merges them into a tight feedback loop:

```
For each claim:
  Hypothesize → Implement → Verify → Execute → Analyze → Decide
                                                    ↓
                              SUPPORTED / PARTIAL (loop) / REFUTED
```

Every line of code serves an experimental purpose. Every experiment tests a specific claim.

## Standards (Mandatory)

| Phase | Standards |
|-------|----------|
| Literature | Coverage, triage, analysis checklists |
| Ideas | RQ, mechanism, identifiability, Claims Matrix, novelty, risk checklists |
| Investigation | Coding standards (karpathy-style) + Experiment standards (6-file contract) |
| Communication | Structure, claims-evidence alignment, figures, citations, writing quality, review checklists |
| Audit | Gate audit, claims verification, citation audit, reproducibility checklists |

## Requirements

- Zotero (optional, for literature management)
- MCP tools: arXiv, paperplain (for literature search)
- Python 3.8+ (for hardware detection script)

## Output

All outputs under `D:/Research/plugin/seek/test/test2/docs/seek/`:
- `phase-0-context/` — Project context, hardware profile
- `phase-1-literature/` — Search log, paper notes, comparison matrix, gap analysis
- `phase-2-ideas/` — Design brief, Claims Matrix v1, novelty report, risk register
- `phase-3-investigation/` — Claims Matrix v2, experiment data (6-file contract), investigation report
- `phase-4-communication/` — Paper plan, figure plan, draft, review log
- `phase-5-audit/` — Gate audit, claims audit, citation audit, reproducibility audit, final verdict

## Origins

Seek merges the best of two plugins:
- **GuideTree** — hierarchical decomposition (Project→Phase→Stage→Step), validation gates, orchestrator state machine, repair-by-reinvocation
- **AutoResearch** — Zotero-first literature, MCP search, 6-file experiment contract, multi-agent blank-context review, Claims-Evidence Matrix, Socratic design interviews

## License

MIT
