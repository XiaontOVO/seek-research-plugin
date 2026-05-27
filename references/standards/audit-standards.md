# Audit Standards

> Violating any hard rule → paper cannot be marked complete.

## Hard Rules

### Gate Audit (Overall Quality Gate)
- [ ] 3 independent Agents reviewed in parallel (Structure + Rigor + Domain)
- [ ] Weighted total score ≥ 6.5/10 (Structure 0.3 + Rigor 0.3 + Domain 0.4)
- [ ] Each Agent's individual score ≥ 3/10
- [ ] All CRITICAL issues resolved

### Claims Audit (Number Verification)
- [ ] Every quantitative claim in the paper has been extracted
- [ ] Every quantitative claim has been cross-checked against raw experiment data (raw_record.json)
- [ ] 7 common failure modes checked:
  1. Number inflation (paper reports higher than raw data)
  2. Best-seed cherry-pick (reports best seed, not mean)
  3. Config mismatch (compared methods used different hyperparameters/data splits)
  4. Aggregation error (claims "average over 5 seeds" but only ran 3)
  5. Delta error ("improves by 15%" but actual calculation differs)
  6. Caption-table mismatch (caption text contradicts figure/table content)
  7. Scope overclaim ("consistently outperforms" but only tested on 2 datasets)
- [ ] Discovered mismatches fixed or flagged as known limitations

### Citation Audit (3-Layer Verification)
- [ ] Layer 1 — Existence: every cited paper is real (DOI/DBLP/CrossRef verified)
- [ ] Layer 2 — Metadata: author, title, year, venue/journal information is correct
- [ ] Layer 3 — Context: the cited content actually supports the claim being made (citation A cannot be cited for claim X if A says the opposite)

### Reproducibility Audit
- [ ] Independent Agent receives: code + config + data + README (no conversation history)
- [ ] Agent attempts to reproduce at least 1 core experiment
- [ ] Independently-run results match paper-reported results (within acceptable error margin)

### Final Verdict
- [ ] All of the following must pass → paper marked COMPLETE
  - Gate Audit: PASS (≥ 6.5)
  - Claims Audit: PASS or WARN (no FAIL)
  - Citation Audit: PASS (no fabricated citations)
  - Reproducibility: PASS (core experiment reproducible)
