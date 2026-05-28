# Self-Check Schema — review_literature

## Input
- [ ] project_context (RQ, constraints, locallit_status)
- [ ] If repair: validation_feedback from prior failed run

## Output Files (must exist on disk)
- [ ] `literature/search-log.md`
- [ ] `literature/comparison-matrix.md`
- [ ] `literature/gap-analysis.md`
- [ ] `literature/paper-notes/` (>= 5 files)

## Output Content
- [ ] **search-log.md**: table with source, query, results count, selected count for EVERY search attempt (including failed/rate-limited)
- [ ] **comparison-matrix.md**: >= 5 rows × 9 columns (Citation | Question | Method | Data | Main Claim | Evidence | Limitation | Relevance | Use As)
- [ ] **gap-analysis.md**: <= 3 sentences (existing work → what's missing → our positioning)
- [ ] **paper-notes/**: one .md per deep-read paper, each with structured sections (RQ, Method, Data, Main Claim, Evidence Strength, Limitations, Relevance, Use As)


## Control Plane Files (MANDATORY — check before valid=true)

```bash
ls guidetree/plan/stage_dags/P*-stage_dag.json 2>/dev/null || echo "MISSING_STAGE_DAG"
ls guidetree/plan/steps/P*.S*-steps.json 2>/dev/null || echo "MISSING_STEP_PLANS"
ls guidetree/registry/artifact_registry.json 2>/dev/null || echo "MISSING_REGISTRY"
ls guidetree/state/execution_history.jsonl 2>/dev/null || echo "MISSING_EXECUTION_LOG"
```
If MISSING_STAGE_DAG or MISSING_REGISTRY -> BLOCKING_ISSUE. Do NOT mark valid=true without control plane files.

## Self-Check
- [ ] LocalLiterature searched before arXiv (LocalLiterature-first)?
- [ ] External search attempted >= 3 keyword combos across all viable tiers?
- [ ] Every search recorded (including failures) in search-log.md?
- [ ] Total unique candidates >= 20?
- [ ] Each candidate has 1-2 sentence triage rationale?
- [ ] Deep-read papers >= 5?
- [ ] Comparison matrix >= 5 rows, all 9 columns filled?
- [ ] Gap analysis is specific to THIS RQ (not generic)?
- [ ] All files exist on disk? Verify: `ls literature/search-log.md literature/comparison-matrix.md literature/gap-analysis.md`
