# Structural Review Prompt
# Agent receives: this prompt + artifact paths. ZERO conversation history.
# Adapted from AutoResearch audit-gate/prompts/structural-review.md

Review the following research artifacts for STRUCTURAL quality.

## Artifacts to Review
{{ARTIFACT_PATHS}}

## Review Criteria

### 1. Completeness
- Are all required sections/components present?
- Is anything obviously missing that would be expected at this stage?

### 2. Logical Flow
- Do arguments build on each other coherently?
- Is the progression of ideas easy to follow?
- Are there gaps in the logical chain?

### 3. Organization
- Are artifacts well-organized with clear sectioning?
- Is the hierarchy of information appropriate?
- Are related items grouped together?

### 4. Format Compliance
- Do outputs follow the expected format conventions?
- Are paths and references correct?
- Is metadata (dates, statuses) present and correct?

## Output Format (JSON)
```json
{
  "structural_score": 0-10,
  "strengths": ["specific strength 1", "specific strength 2"],
  "weaknesses": ["specific weakness 1", "specific weakness 2"],
  "missing_items": ["missing item 1 if any"],
  "issues": [
    {"severity": "CRITICAL|MAJOR|MINOR", "location": "file:section", "issue": "description", "fix": "suggested fix"}
  ],
  "overall_assessment": "one paragraph summary"
}
```
