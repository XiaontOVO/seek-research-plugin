# Experiment Run Layout (6-File Contract)

> Every experiment run MUST produce these 6 files. Adapted from AutoResearch experiment-bridge.

## Directory Structure

```
runs/<experiment-name>/
├── INDEX.yml                    # Experiment index (auto-generated)
├── <run-id>/                    # One directory per run (config × seed combination)
│   ├── raw_record.json          # Complete per-run record
│   ├── attempts.csv             # All attempts (including failures)
│   ├── metrics.csv              # Successful runs only (one row per run)
│   ├── config.yaml              # Resolved complete config
│   ├── hardware_info.json       # Environment fingerprint
│   └── summary.md               # Human-readable run summary
```

## File Specifications

### raw_record.json
```json
{
  "run_id": "exp-c1-seed42",
  "experiment": "exp-c1",
  "seed": 42,
  "timestamp": "2026-05-22T10:30:00Z",
  "metrics": {
    "primary_metric": 0.85,
    "secondary_metrics": {},
    "intermediate_values": {}
  },
  "config_hash": "sha256:...",
  "git_commit": "abc1234"
}
```

### attempts.csv
```csv
attempt,seed,config,timestamp,status,error_message,primary_metric
1,42,configs/exp-c1.yaml,2026-05-22T10:30:00Z,success,,0.85
2,42,configs/exp-c1.yaml,2026-05-22T10:29:00Z,failed,OOM on batch_size=256,
```

### metrics.csv
```csv
seed,config,primary_metric,secondary_metric_1,wall_time_s,gpu_peak_memory_mb
42,configs/exp-c1.yaml,0.85,0.72,120.5,8192
123,configs/exp-c1.yaml,0.83,0.71,118.3,8192
```

### config.yaml
```yaml
experiment: exp-c1
claim: C1
method: "Nova folding verifier"
baseline: "Groth16 batch verification"
batch_sizes: [2, 4, 8, 16, 32, 64, 128]
curve: "BN254"
seeds: [42, 123, 456, 789, 1024]
```

### hardware_info.json
```json
{
  "cpu": "AMD Ryzen 7 H 255",
  "cpu_cores": 16,
  "gpu": "None",
  "ram_gb": 32,
  "os": "Windows 11",
  "python_version": "3.12.10"
}
```

### summary.md
```markdown
# Run Summary: exp-c1-seed42
- **Experiment:** C1 — Gas scaling model
- **Seed:** 42
- **Status:** SUCCESS
- **Primary result:** Nova verifier gas cost = 260K gas at N=1, Groth16 batch = 322K gas (constant)
- **Delta vs baseline:** Nova saves 19.3% at N=1, 66.4% at N=128
```

## Verification
After every run, verify all 6 files exist:
```bash
ls runs/<exp>/<run_id>/raw_record.json runs/<exp>/<run_id>/attempts.csv runs/<exp>/<run_id>/metrics.csv runs/<exp>/<run_id>/config.yaml runs/<exp>/<run_id>/hardware_info.json runs/<exp>/<run_id>/summary.md 2>/dev/null || echo "MISSING_OUTPUT_FILES"
```

If ANY file is missing → BLOCK deployment. Fix code before proceeding.
