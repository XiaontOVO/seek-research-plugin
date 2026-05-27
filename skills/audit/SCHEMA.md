# Self-Check Schema — audit

## Input
- [ ] project_context
- [ ] paper_draft (all .md or .tex files)
- [ ] claims_matrix_v2
- [ ] experiment_data_paths (from investigation_state)
- [ ] If repair: validation_feedback

## Output Files (must exist on disk)
- [ ] `audit/gate-audit.md`
- [ ] `audit/claims-audit.md`
- [ ] `audit/citation-audit.md`
- [ ] `audit/reproducibility-audit.md`
- [ ] `audit/final-verdict.md`

## Output Content
- [ ] **gate-audit.md**: 3-Agent parallel review results (structure ×0.3 + rigor ×0.3 + domain ×0.4), total score, PASS/WARN/FAIL
- [ ] **claims-audit.md**: every quantitative claim extracted, cross-checked against raw_record.json, 7 failure modes checked, per-claim verdict
- [ ] **citation-audit.md**: 3-layer verification (existence → metadata → context), every citation traced, @confidence tags where API unavailable
- [ ] **reproducibility-audit.md**: independent Agent attempt, command run, observed results, match/mismatch with paper
- [ ] **final-verdict.md**: overall PASS/WARN/FAIL, Gold scores per claim (evidence×0.35 + code×0.25 + novelty×0.25 + significance×0.15), zero-GOLD warning if applicable


## Control Plane Files (MANDATORY — check before valid=true)

```bash
ls guidetree/plan/stage_dags/P*-stage_dag.json 2>/dev/null || echo "MISSING_STAGE_DAG"
ls guidetree/plan/steps/P*.S*-steps.json 2>/dev/null || echo "MISSING_STEP_PLANS"
ls guidetree/registry/artifact_registry.json 2>/dev/null || echo "MISSING_REGISTRY"
ls guidetree/state/execution_history.jsonl 2>/dev/null || echo "MISSING_EXECUTION_LOG"
```
If MISSING_STAGE_DAG or MISSING_REGISTRY -> BLOCKING_ISSUE. Do NOT mark valid=true without control plane files.

## Self-Check
- [ ] Gate Audit: 3 Agents dispatched in parallel with zero context? Total >= threshold (7.0)? Each agent >= 3?
- [ ] Claims Audit: every quantitative claim checked against raw data? 7 failure modes checked? No material mismatches?
- [ ] Citation Audit: Layer 1 (all citations exist)? Layer 2 (metadata correct)? Layer 3 (context supports claim)? Fallback attempted before @confidence: likely?
- [ ] Reproducibility: independent Agent ran core experiment? Results match within acceptable error?
- [ ] Final verdict correct: PASS only if all 4 audits pass?
- [ ] Gold scores computed correctly with the formula? Zero-GOLD warning present if no claims >= 0.75?
- [ ] All 5 files exist on disk? Verify with `ls audit/`
