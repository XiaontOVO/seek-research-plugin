# Context Definition Standards

> Violating any hard rule -> research context is incomplete; cannot proceed to literature review.

## Hard Rules

### Research Question
- [ ] Research question stated in one sentence (not a paragraph or a topic area)
- [ ] RQ is specific enough that a third party can identify what is in-scope vs out-of-scope
- [ ] If the RQ requires decomposition, sub-questions are listed

### Falsifiability
- [ ] Falsification condition is explicit and observable ("what observation would disprove the hypothesis")
- [ ] Falsification condition is not circular ("we would see it if it exists" is not a falsification condition)
- [ ] Falsification condition can be tested with available or planned resources

### Constraints
- [ ] Time budget is explicit (even if approximate)
- [ ] Compute budget is explicit (even if "unlimited" — state it)
- [ ] Data availability is assessed (what data exists, what needs to be collected)
- [ ] All constraints that materially affect research scope are documented

### Hardware Profile
- [ ] CPU model and core count recorded
- [ ] GPU model (if any) and VRAM recorded
- [ ] RAM total recorded
- [ ] Available disk space recorded
- [ ] Python version and key libraries recorded

### LocalLiterature Status
- [ ] LocalLiterature directory exists (D:/LocalLiterature/)
- [ ] PDF count and metadata files checked
- [ ] Status recorded: available | missing

### Prior Work Inheritance
- [ ] Prior project directories scanned for GOLD_MANIFEST.md, design-brief.md, experiment data
- [ ] Reusable assets catalogued (methods, baselines, experiment harnesses, lessons learned)
- [ ] Gaps between prior assets and current RQ identified

### Completeness
- [ ] All unanswered questions marked explicitly as `_TODO_` with reason (not silently skipped)
- [ ] No invented answers — vagueness surfaced, not filled in
- [ ] All assumptions labeled with confidence level (confirmed | likely | speculative)
