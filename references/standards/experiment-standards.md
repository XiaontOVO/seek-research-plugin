# Experiment Standards

> Violating any hard rule → experiment results cannot be trusted.

## Hard Rules

### Experiment Design
- [ ] Every experiment has an explicit hypothesis (a one-sentence statement; "let's see what happens" is not an experiment)
- [ ] Every experiment has an explicit success criterion (quantitative threshold, e.g. "> 5% improvement over baseline")
- [ ] Baseline comparison present (cannot run only your own method; at least one baseline)
- [ ] Negative control present (proves signal is not noise — random baseline or shuffled labels)

### Execution
- [ ] Sanity check runs first (small scale / tiny data, verifying end-to-end pipeline passes, no syntax/import errors)
- [ ] Multi-seed runs (minimum 3 different seeds, recommended 5)
- [ ] All attempts recorded (including failures and crashes), written to attempts.csv
- [ ] Same config × seed combination never re-run (check existing results first to avoid wasted compute)

### Output Specification (6-File Contract)
Every experiment run directory must contain these 6 files:

- [ ] `raw_record.json` — Complete per-run record (all metrics, all intermediate values)
- [ ] `attempts.csv` — All attempts (including failed ones, with error messages)
- [ ] `metrics.csv` — Successful-run summary metrics only (one row per successful run)
- [ ] `config.yaml` — Resolved complete config (all hyperparameter final values)
- [ ] `hardware_info.json` — Environment fingerprint (GPU model, driver version, CUDA version, CPU, RAM)
- [ ] `summary.md` — Human-readable run summary (one-sentence result + key numbers)

### Analysis
- [ ] Effect size + significance reported together (no bare p-values; must include effect size like Cohen's d or percentage delta)
- [ ] Delta vs baseline must be reported (absolute difference + relative percentage)
- [ ] Outliers must be flagged and explained (never silently dropped; annotate in summary.md)
- [ ] Plots must have error bars or confidence intervals (no bare mean lines)
