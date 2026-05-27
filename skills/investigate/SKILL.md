---
name: investigate
family: investigation
description: > Claims-driven unified code+experiment loop. Directly incorporates mechanisms from experiment-bridge, experiment-dse, implement-test-driven-development, and plan-todolist. NOT for analytical surveys without code — use literature-survey project type.
---

# investigate

**Core principle:** Code that doesn't run doesn't exist. Deploy early, fail fast. Every experiment tests a specific claim. Every line of code serves an experimental purpose.

## CLI-First Operations (from experiment-bridge)

```bash
# Run experiment via the project's runner
python -m project.runner --config configs/experiment.yaml --backend real
# Or: direct binary execution (Rust, C++, etc.)
cargo run --release -- --circuit sha256 --curve bn254
# Or: ML training
python train.py --config configs/sanity.yaml --seed 42
# Check hardware status
nvidia-smi 2>/dev/null || lscpu | head -10
python -c "import os; print(f'CPU cores: {os.cpu_count()}')"
# Collect and validate results
cat runs/*/metrics.csv | head -20
# Verify 6-file output contract (HARD GATE)
ls runs/<exp>/<run_id>/raw_record.json runs/<exp>/<run_id>/attempts.csv runs/<exp>/<run_id>/metrics.csv runs/<exp>/<run_id>/config.yaml runs/<exp>/<run_id>/hardware_info.json runs/<exp>/<run_id>/summary.md 2>/dev/null || echo "BLOCKED: Missing output files — fix code before proceeding"
```

## Work Stack — What Tool When (from experiment-bridge)

| Task | Tool | Why |
|------|------|-----|
| Run existing experiment (config only) | CLI: `python run_experiment.py --config ...` | No code change needed |
| Modify config/params | CLI: edit YAML/JSON | Data change, not code |
| Small fix (<20 lines, 1 file) | Direct Edit | Overhead of full workflow not justified |
| New experiment code (>20 lines, >1 file) | TDD cycle: RED → GREEN → REFACTOR | Code must be designed, tested |
| Code review before experiment | Agent(blank context) | Fresh eyes on correctness |
| Statistical analysis (ANCOVA, interactions) | Agent(blank context) | Cross-verify statistical reasoning |
| Batch deployment (>=6 jobs) | Queue with OOM-aware retry | Reliable orchestration |
| Parallel execution (<=5 jobs) | Background Bash | Maximize throughput |

**Key boundary:** Writing >20 lines across >1 file → full TDD cycle. Analyzing >2 conditions → dispatch Agent.

## TDD Iron Law (from implement-test-driven-development)

**No production code without a failing test first.** You don't know if you're testing the right thing unless you see the test fail first.

Cycle:
1. **RED:** Write a minimal failing test. Run it. Watch it fail.
2. **GREEN:** Write minimal code to pass. Watch it pass.
3. **REFACTOR:** Improve while keeping green.

Red flags (STOP and restart TDD):
- Writing test after code → STOP. Start RED.
- Test passes without writing code → STOP. Test is wrong.
- Can't figure out how to test → STOP. Interface needs refactoring.

## Phase Plan — Stage/Step Decomposition

Before ANY execution, write the plan to guidetree/plan/:

**Step 0: Write stage DAG**
Write `guidetree/plan/stage_dags/P4-stage_dag.json`:
```json
{
  "phase_id": "P4",
  "phase_name": "Investigation",
  "stages": [
    { "id": "P4.S1", "name": "Setup", "goal": "Establish experimental infrastructure", "depends_on": [] },
    { "id": "P4.S2", "name": "Baseline", "goal": "Implement and validate baselines", "depends_on": ["P4.S1"] },
    { "id": "P4.S3", "name": "Claims", "goal": "Test each claim in dependency order", "depends_on": ["P4.S2"] },
    { "id": "P4.S4", "name": "Finalize", "goal": "Ablation, multi-seed, claims-matrix-v2", "depends_on": ["P4.S3"] }
  ],
  "edges": [["P4.S1","P4.S2"],["P4.S2","P4.S3"],["P4.S3","P4.S4"]]
}
```
→ CHECKPOINT: Write stage DAG NOW. Update `guidetree/project.yaml` current.phase_id = "P4", current.stage_id = "P4.S1".

**For each stage, write step plan** before executing:
Write `guidetree/plan/steps/P4.S1-steps.json`:
```json
{
  "stage_id": "P4.S1",
  "steps": [
    { "id": "P4.S1.S1", "name": "Verify Hardware", "action": "Run detect_hardware.py", "expected_output": "hardware-profile.json" },
    { "id": "P4.S1.S2", "name": "Prioritize Experiments", "action": "Order claims by DAG", "expected_output": "experiment-plan.md" }
  ]
}
```
Write `guidetree/plan/steps/P4.S2-steps.json`, `P4.S3-steps.json`, `P4.S4-steps.json` similarly.

→ CHECKPOINT: Write step plan NOW. Register each step's expected output in `guidetree/registry/artifact_registry.json` BEFORE executing.

**After each step executes**: Update `guidetree/project.yaml` current.step_id. After each stage: update current.stage_id. Log to `guidetree/state/execution_history.jsonl`.

## Output Directory Convention

```bash
# Phase directory
mkdir -p phases/phase-04-investigate/stages/{stage-01-setup,stage-02-baseline/{src,sanity-results},stage-03-claims/{hypothesis-cards,analysis-notes},stage-04-finalize}
mkdir -p phases/phase-04-investigate/runs
```

Write `phases/phase-04-investigate/phase.state.yaml`:
```yaml
phase_id: phase_4_investigate
status: in_progress
current_stage: stage-01-setup
stages_completed: []
```

Write `phases/phase-04-investigate/stages/stage-01-setup/stage.state.yaml`:
```yaml
stage_id: stage-01-setup
phase_id: phase_4_investigate
status: in_progress
```

→ UPDATE `project.state.yaml`: set `current_phase: phase_4_investigate`, `current_stage: stage-01-setup`.

Source code → `stages/stage-02-baseline/src/`. Experiment data → `../runs/<experiment>/` (6-file contract per run). Update each stage's state.yaml when it completes.

## Workflow

### Stage 3.1: Setup

**Step 3.1.1: Verify Hardware**
```bash
nvidia-smi --query-gpu=name,memory.total --format=csv,noheader 2>/dev/null || echo "NO_GPU"
python -c "import os; print(f'CPU: {os.cpu_count()} cores')"
df -h . 2>/dev/null || python -c "import shutil; print(f'Disk free: {shutil.disk_usage(\".\").free // (1024**3)} GB')"
```

**Step 3.1.2: Create Directory Structure and phase.state.yaml**
```bash
mkdir -p analysis/{stage-3.1-setup,stage-3.2-baseline/{src,sanity-results},stage-3.3-claims/{hypothesis-cards,analysis-notes},stage-3.4-finalize,runs}
```
Write `analysis/phase.state.yaml` NOW (before any other work):
```yaml
phase: investigation
current_stage: 3.1-setup
status: in_progress
project_type: computational_experiment
```
Write `runs/INDEX.yml` (empty index).

If project_type is `literature_survey`: SKIP this entire phase. Mark status=skipped, valid=true, and proceed to communicate. Literature surveys synthesize existing work and do not require new code or experiments.

### Stage 3.2: Baseline Implementation

**Step 3.2.1: List Required Baselines**
From Claims Matrix, union all "required_baselines", deduplicate.
Write `stage-3.2-baseline/baselines.yml`. Update phase.state.yaml: `current_stage: 3.2-baseline`.

**Step 3.2.2: Implement Each Baseline (TDD cycle per baseline)**
For EACH baseline, follow the TDD cycle:
1. RED: Write a failing test that checks the baseline produces expected output format
2. GREEN: Write the baseline code following coding-standards.md
3. REFACTOR: Clean up while tests pass

Write code to `stage-3.2-baseline/src/`. Write tests alongside.

**Step 3.2.3: Sanity Check (HARD GATE — from experiment-bridge)**
Run the sanity-stage experiment first (smallest, fastest block):
```bash
python stage-3.2-baseline/src/<baseline>.py --mode sanity --seed 42
```
Verify pipeline works end-to-end. Check 6-file output:
```bash
ls runs/baseline-<name>/seed_42/raw_record.json runs/baseline-<name>/seed_42/attempts.csv runs/baseline-<name>/seed_42/metrics.csv runs/baseline-<name>/seed_42/config.yaml runs/baseline-<name>/seed_42/hardware_info.json runs/baseline-<name>/seed_42/summary.md 2>/dev/null || echo "BLOCKED: Missing output files — code must implement the unified runs/ standard"
```

If sanity fails → auto-debug (max 3 attempts):
1. Parse error output (traceback, stderr, logs, exit code)
2. Diagnose by error type:
   - Build/import error → check toolchain, dependencies, paths
   - Runtime error → check config values, input data, type mismatches
   - Output format error → add missing data recording code
   - Timeout → reduce data size
   - OOM → reduce batch/model/data size
   - NaN/Inf → check division by zero, log(0), uninitialized values
3. Fix and re-run
4. After 3 failures → BLOCK. Report ALL error logs and attempted fixes. Do NOT proceed.

**Step 3.2.4: Run Baseline**
Full baseline run (>= 3 seeds). Results to `runs/baseline-<name>/` with 6-file contract per seed.

### Stage 3.3: Claim Investigation Loop (Per Claim)

For each claim in priority order (from Claims DAG):

**Step N.1: Hypothesis Card**
Write `stage-3.3-claims/hypothesis-cards/<claimID>.md`:
```
Claim: [text]
Hypothesis: If [mechanism], then [quantitative prediction]
Falsification: If [condition], claim is refuted
Success criterion: [quantitative threshold]
Decision boundaries: SUPPORTED if [X], PARTIAL if [Y], REFUTED if [Z]
```

**Step N.2: Implement Experiment Code (TDD)**
Write/modify code ONLY for this claim. Follow TDD cycle:
1. RED: Write failing test
2. GREEN: Write code, pass test
3. REFACTOR: Clean up

Code goes to `stage-3.2-baseline/src/`. Each claim's experiment is a separate entry point.

**Step N.3: Code Review (if >20 lines or new module)**
Send code to Agent(blank context, ZERO conversation history) with:
```
Review this implementation for correctness.
- Hypothesis: [from hypothesis card]
- Code: [diff]
- Check: correctness, coding-standards compliance, logic bugs, reproducibility
Output: CRITICAL/MAJOR/MINOR issues with exact fix locations.
```
CRITICAL → fix and re-review (max 2 rounds). If Agent unavailable → manual review, flag as non_blocking_warning.

**Step N.4: Experimental Design Gate**
Before running: does this experiment actually test the hypothesis? Is the metric appropriate? Are confounds controlled?

**Step N.5: Sanity Check (HARD GATE)**
```bash
python stage-3.2-baseline/src/<experiment>.py --config configs/<claimID>.yaml --seed 42 --sanity
```
Same 6-file verification as Step 3.2.3. Auto-debug max 3 attempts.

**Step N.6: Execute Experiment**
- <= 5 jobs → parallel background Bash
- >= 6 jobs → queue with manifest (see queue_runner.py)
- >= 3 seeds (recommended 5)
- Record ALL attempts (including failures) in attempts.csv
- NEVER re-run identical config × seed combination

**Step N.7: Data Quality Check**
```python
import pandas as pd, numpy as np
df = pd.read_csv("runs/<exp>/metrics.csv")
assert not df.isna().any().any(), "NaN in metrics"
assert not np.isinf(df.select_dtypes(include='number')).any().any(), "Inf in metrics"
print(df.describe())
```
Check: NaN/Inf, convergence, statistical assumptions. Document issues, don't silently drop.

**Step N.8: Analyze Results**
```python
import numpy as np
from scipy import stats
mean_val, std_val = np.mean(metrics), np.std(metrics)
delta_abs = mean_val - baseline_mean
delta_pct = (delta_abs / baseline_mean) * 100
d = (mean_val - baseline_mean) / np.sqrt((np.var(metrics) + np.var(baseline_metrics)) / 2)
t_stat, p_val = stats.ttest_ind(metrics, baseline_metrics)
```
Report: effect size + significance + delta vs baseline. Flag outliers. Compare against hypothesis prediction.
Write `stage-3.3-claims/analysis-notes/<claimID>.md`.

**Step N.9: Decide**
- SUPPORTED: Results match prediction → update Claims Matrix, proceed
- PARTIAL: Direction correct, magnitude insufficient → diagnose, loop back to N.2 (max 5 iterations)
- REFUTED: Results contradict → document negative result, proceed
- DESCOPED: Claim in non_goals → mark descoped, skip
- INCONCLUSIVE: Cannot produce interpretable results → document, flag

**Step N.10: Persist State**
Write `investigation-state.json` with current_claim, iteration, per_claim_status, last_completed_step, checkpoint timestamp.

### Stage 3.4: Finalization

**Step 3.4.1: Ablation Studies (for each supported claim)**
Remove one component at a time, measure delta. Use config flags (don't edit source). Write ablation results.

**Step 3.4.2: Multi-Seed Validation**
If any supported claim < 5 seeds, run additional seeds.

**Step 3.4.3: Produce Claims Matrix v2**
Compile final matrix with all evidence. Write `stage-3.4-finalize/claims-matrix-v2.md`. Write `stage-3.4-finalize/investigation-report.md`.

## HARD GATE — Code and Experiment Execution (Self-Validation)

```bash
# Source code MUST exist for computational experiments
find analysis/stage-3.2-baseline/src/ -name "*.py" -o -name "*.rs" 2>/dev/null | head -3 || echo "NO_SOURCE_CODE"
# Experiment data MUST exist
find analysis/runs/ -name "metrics.csv" 2>/dev/null | head -3 || echo "NO_METRICS"
```

If NO_SOURCE_CODE AND NO_METRICS → **BLOCKING_ISSUE**. The investigation phase requires actual code and experiments. An analytical survey without code is not a valid investigation — use `literature_survey` project_type instead.

If project_type IS `literature_survey`: skip investigation (status=skipped, valid=true). Go directly to communicate.

If code exists: proceed with normal self-validation against experiment-standards.md and coding-standards.md.

## Output

- `stage-3.1-setup/experiment-plan.md`, `stage-3.2-baseline/baselines.yml`
- `stage-3.2-baseline/src/` — all source code
- `stage-3.2-baseline/sanity-results/` — sanity check outputs
- `stage-3.3-claims/hypothesis-cards/`, `stage-3.3-claims/analysis-notes/`, `stage-3.3-claims/decision-log.md`
- `stage-3.4-finalize/claims-matrix-v2.md`, `stage-3.4-finalize/investigation-report.md`
- `runs/INDEX.yml`, `runs/<experiment>/seed_<N>/` (6-file contract each)
- `phase.state.yaml`, `investigation-state.json`
