# Rigor Review Prompt
# Agent receives: this prompt + artifact paths. ZERO conversation history.
# Adapted from AutoResearch audit-gate/prompts/rigor-review.md

Review the following research artifacts for RIGOR and methodological soundness.

## Artifacts to Review
{{ARTIFACT_PATHS}}

## Review Criteria

### 1. Methodology Soundness
- Is the methodology appropriate for the research question?
- Are methods clearly described and reproducible?
- Are assumptions stated and justified?

### 2. Statistical Validity
- Are statistical tests appropriate for the data?
- Are effect sizes reported alongside significance?
- Are sample sizes adequate?
- Are multiple comparisons accounted for?

### 3. Baseline Appropriateness
- Are baselines well-chosen and competitive?
- Are comparisons fair (same data, same compute budget)?
- Are ablation studies comprehensive?

### 4. Limitation Honesty
- Are limitations explicitly discussed?
- Are failure modes acknowledged?
- Are scope claims proportional to evidence?

### 5. Internal Consistency
- Do numbers match across sections?
- Are there contradictions between claims?
- Do conclusions follow from results?

## Output Format (JSON)
```json
{
  "rigor_score": 0-10,
  "strengths": ["specific strength 1"],
  "weaknesses": ["specific weakness 1"],
  "methodology_issues": [{"issue": "...", "severity": "CRITICAL|MAJOR|MINOR"}],
  "statistical_issues": [{"issue": "...", "severity": "CRITICAL|MAJOR|MINOR"}],
  "baseline_issues": [{"issue": "...", "severity": "CRITICAL|MAJOR|MINOR"}],
  "overall_assessment": "one paragraph"
}
```
