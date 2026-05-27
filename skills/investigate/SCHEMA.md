# Self-Check Schema — investigate

## Input
- [ ] project_context (hardware, constraints)
- [ ] design_brief (mechanism, validation plan)
- [ ] claims_matrix v1 (evidence="_pending_")
- [ ] claims-dag.yml (for execution ordering)
- [ ] If repair: validation_feedback

## Output Files (must exist on disk)

### Stage 3.1 Setup
- [ ] `stage-3.1-setup/experiment-plan.md`
- [ ] `stage-3.1-setup/baselines.yml`

### Stage 3.2 Baseline
- [ ] `stage-3.2-baseline/src/` — baseline implementation
- [ ] `stage-3.2-baseline/sanity-results/` — sanity check outputs

### Stage 3.3 Claims
- [ ] `stage-3.3-claims/hypothesis-cards/<claimID>.md` — one per claim
- [ ] `stage-3.3-claims/analysis-notes/<claimID>.md` — one per claim
- [ ] `stage-3.3-claims/decision-log.md`

### Stage 3.4 Finalize
- [ ] `stage-3.4-finalize/claims-matrix-v2.md` — evidence column filled
- [ ] `stage-3.4-finalize/investigation-report.md`

### Runs (6-file contract per experiment per seed)
- [ ] `runs/INDEX.yml`
- [ ] `runs/<experiment>/seed_<N>/raw_record.json`
- [ ] `runs/<experiment>/seed_<N>/attempts.csv`
- [ ] `runs/<experiment>/seed_<N>/metrics.csv`
- [ ] `runs/<experiment>/seed_<N>/config.yaml`
- [ ] `runs/<experiment>/seed_<N>/hardware_info.json`
- [ ] `runs/<experiment>/seed_<N>/summary.md`

### State
- [ ] `phase.state.yaml` — current_stage tracking
- [ ] `investigation-state.json` — per-claim progress, for recovery

## Output Content
- [ ] **claims-matrix-v2.md**: every claim has final status (`supported | partial | refuted | descoped | inconclusive`), supported claims have evidence pointer to concrete data
- [ ] **investigation-report.md**: summary (N supported, M partial, K refuted), key findings per claim, paper recommendations


## Control Plane Files (MANDATORY — check before valid=true)

```bash
ls guidetree/plan/stage_dags/P*-stage_dag.json 2>/dev/null || echo "MISSING_STAGE_DAG"
ls guidetree/plan/steps/P*.S*-steps.json 2>/dev/null || echo "MISSING_STEP_PLANS"
ls guidetree/registry/artifact_registry.json 2>/dev/null || echo "MISSING_REGISTRY"
ls guidetree/state/execution_history.jsonl 2>/dev/null || echo "MISSING_EXECUTION_LOG"
```
If MISSING_STAGE_DAG or MISSING_REGISTRY -> BLOCKING_ISSUE. Do NOT mark valid=true without control plane files.

## Self-Check
- [ ] Every experiment tests a specific claim (no orphan experiments)?
- [ ] Sanity check passed before full execution?
- [ ] >= 3 seeds per experiment?
- [ ] All attempts logged (including failures)?
- [ ] 6-file contract complete for every run?
- [ ] Effect size + significance reported for every claim?
- [ ] Delta vs baseline reported?
- [ ] No claim marked SUPPORTED with insufficient evidence (simulation-only, qualitative-only)?
- [ ] Negative results documented for refuted claims?
- [ ] Coding-standards.md all hard rules checked?
- [ ] Experiment-standards.md all hard rules checked?
- [ ] Claims DAG execution order respected (dependencies before dependents)?
- [ ] All files exist on disk? Verify stage directories.
