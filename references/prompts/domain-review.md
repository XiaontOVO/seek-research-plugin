# Domain Review Prompt
# Agent receives: this prompt + artifact paths + domain dimensions. ZERO conversation history.
# Adapted from AutoResearch audit-gate/prompts/domain-review-gate<N>.md

Review the following research artifacts for DOMAIN-SPECIFIC quality.

## Artifacts to Review
{{ARTIFACT_PATHS}}

## Domain Dimensions to Check
{{DOMAIN_DIMENSIONS}}

## Review Criteria

### 1. Literature Positioning
- Is the work correctly positioned against prior art?
- Are key papers in the domain cited?
- Is the novelty claim credible given the literature?

### 2. Technical Accuracy
- Are domain-specific concepts used correctly?
- Are technical claims accurate?
- Is terminology consistent with domain conventions?

### 3. Contribution Significance
- Does this work advance the field?
- Is the contribution proportionate to the claims?
- Would a domain expert find this meaningful?

### 4. Gap Coverage
- Does the work address the identified research gap?
- Are there unaddressed aspects of the gap?
- Is the contribution scoped appropriately?

## Output Format (JSON)
```json
{
  "domain_score": 0-10,
  "strengths": ["specific strength 1"],
  "weaknesses": ["specific weakness 1"],
  "positioning_issues": [{"issue": "...", "severity": "CRITICAL|MAJOR|MINOR"}],
  "accuracy_issues": [{"issue": "...", "severity": "CRITICAL|MAJOR|MINOR"}],
  "significance_assessment": "one paragraph on contribution significance",
  "overall_assessment": "one paragraph"
}
```
