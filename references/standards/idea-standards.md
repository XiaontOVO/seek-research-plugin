# Idea Design Standards

> Violating any hard rule → research design is incomplete; cannot proceed to investigation.

## Hard Rules

### Research Question
- [ ] RQ stated in one sentence (not a paragraph)
- [ ] RQ is falsifiable ("what observation would disprove my hypothesis" has a clear answer)
- [ ] RQ scope is answerable in one research project (not "solve AI" level)

### Mechanism & Causality
- [ ] Expected mechanism has a causal chain (A → B → C → expected outcome)
- [ ] The most uncertain link in the causal chain is annotated
- [ ] Alternative explanations (confounders) are listed and discussed

### Identifiability
- [ ] A discriminating condition exists to distinguish your mechanism from alternatives ("if mechanism A, see X; if mechanism B, see Y")
- [ ] Plan for handling missing key data exists

### Validation Plan
- [ ] Primary metric defined, with justification for why it captures the RQ
- [ ] Baseline defined, with explanation of what floor it establishes
- [ ] Negative control defined, with explanation of what confound it rules out

### Claims Matrix
- [ ] At least 2 testable claims
- [ ] Each claim has:
  - Hypothesis (one sentence)
  - Quantitative prediction (specific number + range)
  - Verification method (what experiment)
  - Required baseline (what comparison to implement)
  - Falsification condition (what result would refute this claim)

### Novelty
- [ ] Novelty verified (at minimum: arXiv + Semantic Scholar searched)
- [ ] Difference from closest prior work expressed in 1-2 sentences
- [ ] If prior precedent exists → claim adjusted to reflect the difference

### Risk Register
- [ ] At least 3 risks identified
- [ ] Each risk has: early-warning signal (what to look for first) + mitigation plan (what to do)
- [ ] Fatal risks (project-killing) vs. delaying risks are distinguished
