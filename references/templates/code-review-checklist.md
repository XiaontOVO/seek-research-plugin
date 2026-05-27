# Agent Code Review Checklist

> Send this checklist to blank-context Agents for code review. Agent receives: code diff + hypothesis card + this checklist + coding-standards.md. ZERO conversation history.

## Review Instructions

Review the following implementation for correctness and standards compliance.

## Experiment Plan Context
[PASTE relevant experiment plan section]

## Method Description
[PASTE from hypothesis card]

## Implementation
[PASTE code diff]

## Check For

### 1. Correctness (CRITICAL if violated)
- [ ] Does code correctly implement the experiment described in the plan?
- [ ] Are all parameters from the plan reflected in the code?
- [ ] Are random seeds fixed and documented?
- [ ] Is the output format correct and schema-valid?

### 2. Logic & Edge Cases (CRITICAL or MAJOR)
- [ ] Logic bugs, off-by-one errors, incorrect conditions?
- [ ] Missing error handling for edge cases?
- [ ] Unhandled failure modes (timeout, OOM, NaN, division by zero)?
- [ ] Race conditions in parallel execution?

### 3. Reproducibility (CRITICAL if violated)
- [ ] Fixed seeds (not system-time-based)?
- [ ] Documented environment (hardware, dependencies)?
- [ ] All hyperparameters in a single config file?
- [ ] Results written to structured files (JSON/CSV), not stdout?

### 4. Coding Standards (MAJOR if violated)
- [ ] Type annotations on every function?
- [ ] E2E test present?
- [ ] Single function <= 50 lines? Single file <= 300 lines?
- [ ] Self-explanatory variable names (no x, tmp, data)?
- [ ] Named constants for magic numbers?
- [ ] No unnecessary abstraction? No copy-paste?

### 5. Experiment-Specific (MAJOR if violated)
- [ ] 6-file output contract implemented?
- [ ] All attempts recorded (including failures)?
- [ ] No duplicate config x seed combinations?
- [ ] Ablation controlled via config, not source edits?

## Verdict

For each issue: **CRITICAL / MAJOR / MINOR** with exact fix location and suggested fix.

- CRITICAL → fix and re-review (max 2 rounds)
- MAJOR → fix before experiment execution
- MINOR → log, fix when convenient
