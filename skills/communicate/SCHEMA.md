# Self-Check Schema — communicate

## Input
- [ ] project_context (RQ, constraints)
- [ ] claims_matrix_v2 (evidence filled)
- [ ] investigation_report (key findings)
- [ ] investigation_state (experiment data paths)
- [ ] If repair: validation_feedback

## Output Files (must exist on disk)
- [ ] `paper/paper-plan.md`
- [ ] `paper/figure-plan.md`
- [ ] `paper/draft/manuscript.md` (or .tex)
- [ ] `paper/review-log.md`
- [ ] `paper/review-state.json` (for recovery)

## Output Content
- [ ] **paper-plan.md**: paper type, section structure (5-8), per-section claims + evidence + citations + figures
- [ ] **figure-plan.md**: every figure/table with ID, type, data source, take-away message, priority (MUST-HAVE/NICE-TO-HAVE)
- [ ] **draft/**: 5-8 sections, abstract self-contained, intro answers What/Why/So What, hero figure present
- [ ] **review-log.md**: >= 1 review round, each with score, CRITICAL/MAJOR/MINOR issues, fixes applied


## Control Plane Files (MANDATORY — check before valid=true)

```bash
ls guidetree/plan/stage_dags/P*-stage_dag.json 2>/dev/null || echo "MISSING_STAGE_DAG"
ls guidetree/plan/steps/P*.S*-steps.json 2>/dev/null || echo "MISSING_STEP_PLANS"
ls guidetree/registry/artifact_registry.json 2>/dev/null || echo "MISSING_REGISTRY"
ls guidetree/state/execution_history.jsonl 2>/dev/null || echo "MISSING_EXECUTION_LOG"
```
If MISSING_STAGE_DAG or MISSING_REGISTRY -> BLOCKING_ISSUE. Do NOT mark valid=true without control plane files.

## Self-Check
- [ ] Every paper claim maps to Claims Matrix evidence?
- [ ] Every supported matrix claim appears in paper?
- [ ] No orphan paper claims (not in matrix)?
- [ ] Abstract self-contained (problem + method + 1 quantitative result + significance)?
- [ ] Introduction answers What, Why, So What by the end?
- [ ] Hero figure (Figure 1) shows core contribution?
- [ ] Every figure has a take-away message?
- [ ] All quantitative results have baseline context?
- [ ] No hype words without ironclad evidence?
- [ ] Limitations >= 3 specific items?
- [ ] >= 1 round of Agent review performed (score >= 6/10 or verdict="accept")?
- [ ] All files exist on disk? Verify with `ls`
