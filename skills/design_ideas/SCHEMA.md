# Self-Check Schema — design_ideas

## Input
- [ ] project_context (RQ, constraints, non_goals)
- [ ] literature_review (comparison_matrix, gap_analysis)
- [ ] If repair: validation_feedback

## Output Files (must exist on disk)
- [ ] `ideas/design-brief.md`
- [ ] `ideas/claims-dag.yml` ★ REQUIRED
- [ ] `ideas/claims-matrix.md` (v1, evidence="_pending_")
- [ ] `ideas/novelty-report.md`
- [ ] `ideas/risk-register.md`

## Output Content
- [ ] **design-brief.md**: 5 segments (RQ sharpening, mechanism, identifiability, validation plan, risk register)
- [ ] **claims-dag.yml**: every claim listed with depends_on array, type (main/analysis/secondary/synthesis), no cycles
- [ ] **claims-matrix.md**: >= 2 claims, each with: claim_text, hypothesis, quantitative_prediction, verification_method, required_baselines, required_experiments, falsification_condition, evidence="_pending_", status=pending
- [ ] **novelty-report.md**: per-claim novelty score (0-1), closest prior work, cross-model Agent assessment
- [ ] **risk-register.md**: >= 3 risks, each with early_warning + mitigation, fatal vs delaying distinguished


## Control Plane Files (MANDATORY — check before valid=true)

```bash
ls guidetree/plan/stage_dags/P*-stage_dag.json 2>/dev/null || echo "MISSING_STAGE_DAG"
ls guidetree/plan/steps/P*.S*-steps.json 2>/dev/null || echo "MISSING_STEP_PLANS"
ls guidetree/registry/artifact_registry.json 2>/dev/null || echo "MISSING_REGISTRY"
ls guidetree/state/execution_history.jsonl 2>/dev/null || echo "MISSING_EXECUTION_LOG"
```
If MISSING_STAGE_DAG or MISSING_REGISTRY -> BLOCKING_ISSUE. Do NOT mark valid=true without control plane files.

## Self-Check
- [ ] RQ is falsifiable (not "see what happens")?
- [ ] Every claim has quantitative prediction + falsification condition?
- [ ] Claims DAG valid (no cycles, dependencies resolve)?
- [ ] External critical review (devil's advocate Agent) performed?
- [ ] Novelty verified: all core claims >= NOVELTY_THRESHOLD (0.7) or adjusted?
- [ ] >= 3 risks with early-warning + mitigation?
- [ ] No claims address project non_goals?
- [ ] All 5 files exist on disk? Verify with `ls`
