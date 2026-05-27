# Self-Check Schema — crystallize

## Input
- [ ] project_context
- [ ] claims_matrix_v2
- [ ] investigation_state (experiment data paths)
- [ ] audit_report (gate, claims, citation, reproducibility results)

## Output Files (must exist on disk)
- [ ] `gold/GOLD_MANIFEST.md`
- [ ] `gold/GOLD_INDEX.md`
- [ ] `gold/code/` — all referenced source files (copied, not symlinked)
- [ ] `gold/data/` — experiment-summary.json + key records
- [ ] `gold/meta/` — lessons learned, audit summary, project template

## Output Content
- [ ] **GOLD_MANIFEST.md**: executive summary, per-item scoring (evidence×0.35 + code×0.25 + novelty×0.25 + significance×0.15), classification (GOLD >= 0.75, SILVER >= 0.5, BRONZE >= 0.3, ASPIRATION < 0.3), vulnerability map
- [ ] **GOLD_INDEX.md**: claim → file:line mapping for every gold/silver claim
- [ ] **code/**: all source files referenced in the manifest, actual copies
- [ ] **data/**: experiment-summary.json (Python-aggregated, not grep), at least 1 record per claim
- [ ] **meta/**: audit methodology (bugs found), experiment harness patterns, architecture decisions, lessons learned ("if we did it again"), project template for next research


## Control Plane Files (MANDATORY — check before valid=true)

```bash
ls guidetree/plan/stage_dags/P*-stage_dag.json 2>/dev/null || echo "MISSING_STAGE_DAG"
ls guidetree/plan/steps/P*.S*-steps.json 2>/dev/null || echo "MISSING_STEP_PLANS"
ls guidetree/registry/artifact_registry.json 2>/dev/null || echo "MISSING_REGISTRY"
ls guidetree/state/execution_history.jsonl 2>/dev/null || echo "MISSING_EXECUTION_LOG"
```
If MISSING_STAGE_DAG or MISSING_REGISTRY -> BLOCKING_ISSUE. Do NOT mark valid=true without control plane files.

## Self-Check
- [ ] Max 3 GOLD (more means not selective enough)?
- [ ] Every GOLD traces to experiment run + source file + line number?
- [ ] Evidence folder self-contained (zippable, no external references)?
- [ ] No symlinks — actual file copies?
- [ ] Vulnerability map covers evidence/code/novelty/significance risks?
- [ ] Meta-lessons documented (bugs, patterns, decisions, lessons, template)?
- [ ] All files exist on disk? Verify `ls gold/`
