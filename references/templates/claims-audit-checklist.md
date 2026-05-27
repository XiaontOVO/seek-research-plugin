# Claims Audit Checklist

> Send this checklist to a blank-context Agent for claims verification. Agent receives: paper claims (extracted text) + ALL raw experiment data files (raw_record.json, metrics.csv). ZERO summaries, ZERO interpretations, ZERO conversation history.

## Review Instructions

Extract EVERY quantitative claim from the paper. For each, locate the corresponding evidence in the raw experiment data files. Report per-claim verification.

## 7 Failure Modes (Check Each Claim Against All 7)

### 1. Number Inflation
- [ ] Is the paper value higher than the raw data value by more than standard rounding?
- Rounding rule: only standard rounding to displayed precision is allowed.
- Example: 84.7% → 85% is OK. 84.7% → 85.3% is NOT OK.

### 2. Best-Seed Cherry-Pick
- [ ] Does the paper report the best of N seeds without disclosing it's the best, not the mean?
- If multi-seed: paper must report mean ± std. Reporting max without disclosure = FAIL.

### 3. Config Mismatch
- [ ] Did compared methods use the SAME hyperparameters, datasets, and data splits?
- Different configs for different methods without justification = FAIL.

### 4. Aggregation Error
- [ ] Does the paper claim "average over K seeds" but result files show fewer than K runs?
- Mismatch between claimed and actual seed count = FAIL.

### 5. Delta Error
- [ ] Does the paper say "improves by X%" but the actual delta computes differently?
- Verify: (method - baseline) / baseline × 100 matches the paper's claimed percentage.

### 6. Caption-Table Mismatch
- [ ] Does the figure/table caption describe something different from what the figure/table actually shows?
- Cross-check caption text against figure/table data source.

### 7. Scope Overclaim
- [ ] Does the paper say "consistently outperforms" / "robustly" / "always" but only tested on N datasets?
- Rule: tested on <= 2 datasets → cannot claim "consistently". Tested on <= 1 domain → cannot claim "general".

## Per-Claim Output Format

```yaml
- claim_id: "C1"
  location: "Section 5.1, paragraph 2"
  paper_text: "recursive proofs reduce gas cost by 150x"
  paper_value: "150x"
  evidence_file: "runs/exp-c1-native/raw_record.json"
  evidence_value: "150.2x"
  status: exact_match | rounding_ok | ambiguous_mapping | missing_evidence | config_mismatch | aggregation_mismatch | number_mismatch | scope_overclaim | unsupported_claim
  details: "Paper says 150x, raw data shows 150.2x at N=100. Rounding to 150x is acceptable."
```

## Verdict Decision Table

| Input State | Verdict | reason_code |
|---|---|---|
| No numeric claims in paper | NOT_APPLICABLE | no_numeric_claims |
| Numeric claims, no raw data files | BLOCKED | no_raw_evidence |
| All claims reconcile to raw data | PASS | all_numbers_match |
| Minor rounding drift only | WARN | rounding_drift |
| Any material mismatch | FAIL | claim_mismatch |

## SHA256 Rule

Hash the exact files consumed: `sha256sum <file>` (Linux/Mac) or `Get-FileHash <file> -Algorithm SHA256` (Windows). Record hashes in the audit report for traceability.
