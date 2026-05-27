# Self-Check Schema — discover_ideas

## Input
- [ ] project_context (RQ, constraints, hardware, non_goals)
- [ ] literature_review (comparison_matrix, gap_analysis)
- [ ] If repair: validation_feedback

## Output Files (must exist on disk)
- [ ] `ideas/idea-candidates.md` — ranked candidate ideas with scores
- [ ] `ideas/pilot-results.md` — pilot experiment results (if run)
- [ ] `ideas/selected-idea.md` — the selected top idea for design

## Output Content
- [ ] **idea-candidates.md**: 8-12 generated ideas, each with: summary, hypothesis, min viable experiment, contribution type, risk level, estimated GPU-hours
- [ ] Filtered list: 4-6 surviving after feasibility/novelty/impact checks
- [ ] Deep validation: per-idea novelty assessment, devil's advocate review, ranking
- [ ] **pilot-results.md**: GPU, time, key metric, signal for top 2-3 ideas (if GPU available)
- [ ] **selected-idea.md**: the top-ranked idea with justification, recommended next step


## Control Plane Files (MANDATORY — check before valid=true)

```bash
ls guidetree/plan/stage_dags/P*-stage_dag.json 2>/dev/null || echo "MISSING_STAGE_DAG"
ls guidetree/plan/steps/P*.S*-steps.json 2>/dev/null || echo "MISSING_STEP_PLANS"
ls guidetree/registry/artifact_registry.json 2>/dev/null || echo "MISSING_REGISTRY"
ls guidetree/state/execution_history.jsonl 2>/dev/null || echo "MISSING_EXECUTION_LOG"
```
If MISSING_STAGE_DAG or MISSING_REGISTRY -> BLOCKING_ISSUE. Do NOT mark valid=true without control plane files.

## Self-Check
- [ ] Ideas grounded in literature gaps (not random)?
- [ ] 8-12 ideas generated before filtering?
- [ ] First-pass filter eliminated ideas needing > 1 week GPU or unavailable data?
- [ ] Deep validation performed on 4-6 surviving ideas?
- [ ] Devil's advocate review for each surviving idea?
- [ ] Pilot experiments attempted for top 2-3 (or documented as skipped with reason)?
- [ ] Selected idea clearly marked with justification?
- [ ] All files exist on disk?
