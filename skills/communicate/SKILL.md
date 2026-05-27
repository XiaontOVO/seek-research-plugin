---
name: communicate
family: communication
description: > Claims Matrix → paper pipeline. Transforms the verified Claims-Evidence Matrix v2 into a structured academic paper: plan → figures → write → internal review (max 4 rounds, blank-context Agent each round). Invoked by orchestrator after investigation completes. NOT for running experiments — use investigate. NOT for auditing — use audit.
---

# communicate

**Core principle:** The Claims Matrix writes the paper. You are the translator, not the author. No paper claim without matrix evidence. No evidence without paper representation.

Phase 4 of the Seek pipeline. Transforms the verified Claims Matrix (v2) into a structured paper. Every paper claim maps to matrix evidence. Every evidence entry supports a paper claim.

## When To Use

Trigger phrases:
- "Write the paper" / "draft the manuscript"
- "Plan the paper structure"
- Invoked by orchestrator after Phase 3 (investigate) completes.

## NOT For

- Running experiments or collecting data — use `seek:investigate`
- Literature review — use `seek:review_literature`
- Final audit — use `seek:audit`

## Standards

Before any action, load `references/standards/writing-standards.md`. Every checklist item is a hard constraint.

## Output Directory Convention

All paths from `references/paths.yml`. Before any work, create the output directory:

```bash
mkdir -p paper/draft
```

## Workflow

### Step 0: Pre-Flight Checks
Verify investigation output exists:
```bash
ls analysis/claims-matrix-v2.md analysis/investigation-report.md 2>/dev/null && echo "INVESTIGATION_OK" || echo "INVESTIGATION_MISSING"
```
If INVESTIGATION_MISSING → blocking_issue. Cannot write paper without investigation results.

### Step 1: Load Inputs
- project_context (RQ, constraints)
- claims_matrix_v2 (THE SOURCE OF TRUTH — every claim with evidence)
- investigation_report (key findings, recommendations)
- investigation_state (experiment data paths for figures/tables)
- If repair: validation_feedback

### Step 2: Build Paper Skeleton from Claims Matrix

**Determine paper type:** empirical / theoretical / method / survey.
This determines section structure (5-8 sections).

**Map claims to sections:**
- Each supported claim → core argument in the paper.
- Each partial claim → supplementary or appendix.
- Each refuted claim → honest reporting in limitations.

**Define hero figure (Figure 1):** What one figure shows the core contribution at a glance? Describe what to plot, which methods to compare, what the visual difference should demonstrate.

Write `paper/paper-plan.md`.

### Step 3: Section-by-Section Planning

For each section, specify: goal, key claims covered, evidence referenced, key citations needed, figure/table placements, estimated length.

Standard sections (adapt to paper type): Abstract, Introduction, Related Work, Method, Experimental Setup, Results, Discussion, Limitations, Conclusion.

### Step 4: Figure and Table Plan

For every figure/table: ID, type, description, data source (which experiment/metric), take-away message, priority (MUST-HAVE / NICE-TO-HAVE).

Write `paper/figure-plan.md`.

### Step 5: Write Manuscript

Writing rules:
- Front-load: contribution clear from title, abstract, intro, hero figure.
- One coherent technical story.
- Claims Matrix drives content — no claims not in the matrix.
- Evidence strength drives language: strong → confident, weak → hedged.
- Every quantitative result has baseline context.
- No hype words without ironclad evidence.
- One paragraph <= 15 lines.

Write draft to `paper/draft/`.

### Step 6: Internal Review (Max 4 Rounds, with State Recovery)

Each round = fresh blank-context Agent:
```
Agent receives: paper draft + claims_matrix_v2 + writing-standards.md
Agent receives ZERO conversation history.
Agent scores: logical flow, claims-evidence alignment, missing experiments, positioning, page budget, front-matter strength.
```

Apply fixes for all CRITICAL and MAJOR issues. Continue until score >= 6/10 or verdict = "accept" or 4 rounds exhausted.

**Review State Recovery (from audit-review):**

After each round, persist state to `paper/review-state.json`:
```json
{
  "current_round": 2,
  "max_rounds": 4,
  "rounds": [
    {"round": 1, "score": 5.2, "critical_count": 3, "major_count": 5, "verdict": "revise"},
    {"round": 2, "score": null, "status": "in_progress"}
  ],
  "stopping_condition": "score >= 6.0 or verdict == 'accept'",
  "fix_priority": "code > text > figures > structure",
  "checkpoint": "2026-05-21T10:30:00Z"
}
```

If interrupted, recover from `review-state.json`: resume from current_round, re-read paper draft, apply pending fixes.

Log every round to `paper/review-log.md`.

### Step 7: Self-Validate

Load `references/standards/writing-standards.md`. Check EVERY item:
- [ ] Paper type determined? 5-8 section structure?
- [ ] Abstract self-contained?
- [ ] Introduction answers What, Why, So What?
- [ ] Every paper claim has matrix evidence?
- [ ] Every supported matrix claim in paper?
- [ ] Every figure has take-away message?
- [ ] Hero figure shows core finding?
- [ ] All figures from experiment data?
- [ ] Every citation in Zotero?
- [ ] Prior work from comparison matrix cited?
- [ ] No hype words?
- [ ] Quantitative results have baseline context?
- [ ] Limitations >= 3 specific items?
- [ ] >= 1 round Agent review? All MAJOR resolved? Score >= 6/10?

Unchecked → blocking_issues. Non-goal compliance:
- [ ] Paper does not claim contributions in areas listed as non_goals?
- [ ] Paper scope matches the project scope?

Return valid: true only if ALL items checked AND output files exist on disk AND non-goal compliant.
Verify with: `ls paper/paper-plan.md paper/figure-plan.md paper/draft/*.md paper/review-log.md`.
Missing files → blocking_issue.

### Step 8: Update State

Update `guidetree/project.yaml`:
- phases.communication.status = "done"
- phases.communication.valid = (true/false)
- phases.communication.artifacts = { paper_plan, figure_plan, draft, review_log }
- If valid: set current_phase = "audit"

## Output

- `paper/paper-plan.md`
- `paper/figure-plan.md`
- `paper/draft/` — manuscript
- `paper/review-log.md`

## Next Skill

After this skill: `seek:audit`
