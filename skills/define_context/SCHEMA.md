# Self-Check Schema — define_context

## Input
- [ ] User's research description (raw text)
- [ ] Hardware profile (from detect_hardware.py or manual)
- [ ] LocalLiterature status (checked via ls D:/LocalLiterature/)

## Output Files (must exist on disk)
- [ ] `guidetree/context/project-context.md`
- [ ] `guidetree/context/hardware-profile.json`

## Output Content (in project-context.md)
- [ ] **research_question**: one sentence
- [ ] **falsification_condition**: what observation disproves the hypothesis
- [ ] **constraints**: time budget, compute budget, data availability (each explicit)
- [ ] **non_goals**: things deliberately out of scope
- [ ] **hardware_profile**: CPU, GPU, RAM, disk
- [ ] **locallit_status**: `available | missing`
- [ ] **prior_work**: inherited assets or "none found"
- [ ] **unanswered_questions**: each marked `_TODO_` with reason
- [ ] **assumptions**: each tagged `confirmed | likely | speculative`

## Self-Check
- [ ] RQ is falsifiable (falsification condition is observable and non-circular)?
- [ ] No invented answers — vagueness surfaced, not filled in?
- [ ] All constraints explicit (not "no constraints")?
- [ ] Hardware profile complete (CPU, GPU, RAM, disk, Python version)?
- [ ] LocalLiterature status checked via actual directory listing?
- [ ] Prior projects scanned (even if none found)?
- [ ] All files exist on disk? Verify: `ls guidetree/context/*`

## Control Plane Files (MANDATORY — check before valid=true)

```bash
ls guidetree/plan/stage_dags/P0-stage_dag.json 2>/dev/null || echo "MISSING_STAGE_DAG"
ls guidetree/plan/steps/P0.S*-steps.json 2>/dev/null || echo "MISSING_STEP_PLANS"
ls guidetree/registry/artifact_registry.json 2>/dev/null || echo "MISSING_REGISTRY"
ls guidetree/state/execution_history.jsonl 2>/dev/null || echo "MISSING_EXECUTION_LOG"
```
If MISSING_STAGE_DAG or MISSING_REGISTRY → BLOCKING_ISSUE. Do NOT mark valid=true without control plane files.
