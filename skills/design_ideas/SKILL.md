---
name: design_ideas
family: ideas
description: > 5-segment Socratic design interview + novelty verification + Claims-Evidence Matrix v1. Grounds ideas in literature gaps, verifies novelty via cross-model Agent, builds the Claims Matrix that drives all investigation. Invoked by orchestrator after literature review completes. NOT for running experiments — use investigate. NOT for literature search — use review_literature.
---

# design_ideas

**Core principle:** A claim without a falsification condition and a quantitative prediction is not a claim — it's wishful thinking.

Phase 2 of the Seek pipeline. Guides the researcher through structured problem framing, verifies novelty against prior work, and builds the Claims-Evidence Matrix v1 that will drive all subsequent investigation.

## When To Use

Trigger phrases:
- "Design my research study" / "frame my research question"
- "Help me think through what to test"
- "Build a design brief" / "sharpen my hypothesis"
- Invoked by orchestrator after Phase 1 (review_literature) completes.

## NOT For

- Generating ideas from scratch without literature grounding — complete Phase 1 first
- Writing code or running experiments — use `seek:investigate`
- Literature comparison — use `seek:review_literature`
- Writing manuscripts — use `seek:communicate`

## Standards

Before any action, load `references/standards/idea-standards.md`. Every checklist item is a hard constraint.

## Output Directory Convention

All paths from `references/paths.yml`. Before any work, create the output directory:

```bash
mkdir -p ideas
```

## Workflow

### Step 0: Pre-Flight Checks
Verify required inputs from prior phases exist:
```bash
ls guidetree/context/project-context.md 2>/dev/null && echo "CONTEXT_OK" || echo "CONTEXT_MISSING"
ls literature/comparison-matrix.md literature/gap-analysis.md 2>/dev/null && echo "LITERATURE_OK" || echo "LITERATURE_MISSING"
```
If CONTEXT_MISSING or LITERATURE_MISSING → blocking_issue. Ideas cannot be designed without context and literature foundation.

### Step 1: Load Inputs
- project_context (RQ, constraints, hardware)
- literature_review (comparison_matrix, gap_analysis) — grounds ideas in literature gaps
- If repair: validation_feedback

### Step 2: Convergent Design — 5-Segment Socratic Interview

Max 3 rounds per segment. If unclear after 3 rounds, record best-effort with `_STALLED_`.

**Segment 1: RQ Sharpening**
- "Restate your RQ in one sentence."
- "What observation would falsify it?"
- "Is the scope answerable in one study?"

**Segment 2: Expected Mechanism**
- "Through what mechanism do you expect the result?"
- "What intermediate states would support this mechanism?"
- "Which causal links are you most/least confident about?"

**Segment 3: Identifiability Check**
- "What discriminating condition separates your mechanism from alternatives?"
- "What confounders could produce the same observation?"
- "If key data is missing, how will you handle it?"

**Segment 4: Validation Plan**
- "What is the primary metric, and why does it capture the RQ?"
- "What baseline establishes the floor?"
- "What negative control catches confounders?"

**Segment 5: Risk Register**
- "What are 3-5 biggest things that could kill this project?"
- "For each: earliest warning signal + mitigation."
- "Which are fatal vs. merely delaying?"

### Step 3: Build Claims Dependency DAG

Before writing the matrix, model dependencies between claims:
```yaml
claims_dag:
  C1: { depends_on: [], type: main }
  C2: { depends_on: [], type: main }
  C3: { depends_on: [C1, C2], type: analysis }  # Curve dependency analysis needs C1+C2 results
  C4: { depends_on: [C1], type: secondary }      # Calldata analysis needs C1 gas data
  C5: { depends_on: [C1, C3, C4], type: synthesis }  # Economic model needs all above
```

Rules:
- Main claims (no dependencies) are investigated first
- Dependency claims only investigated after their dependencies resolve
- If a dependency claim is REFUTED, dependent claims may need redesign
- Circular dependencies are forbidden (must be a DAG)

### Step 4: Build Claims-Evidence Matrix v1

From the interview outputs, extract testable claims. For each claim:

| Field | Description |
|-------|-------------|
| claim_id | C1, C2, C3... |
| claim_text | One-sentence claim for the paper |
| hypothesis | Testable sub-hypothesis |
| quantitative_prediction | Specific + range (e.g., ">= 5% improvement") |
| verification_method | What experiment tests this |
| required_baselines | What comparisons are needed |
| required_experiments | Experiment IDs |
| falsification_condition | What result refutes this claim |
| evidence | `_pending_` (Phase 3 fills this) |
| status | pending |

Minimum 2 claims. Each must be independently testable.

Write to `ideas/claims-matrix.md`.

### Step 5: External Critical Review (from idea-discover)

Before novelty verification, get an external review of the design brief.
Dispatch a blank-context Agent as "devil's advocate":
```
Agent receives: design-brief.md + comparison-matrix.md + gap-analysis.md
Agent receives ZERO conversation history.
Agent task: "Find the 3 weakest points in this research design. For each:
  - What could go wrong?
  - What assumption is most questionable?
  - If you were a reviewer, what would you reject this for?"
```
Apply critical feedback to strengthen the design before novelty check.
If Agent unavailable → note as non_blocking_warning, proceed with self-review.

### Step 6: Novelty Verification (Hard Gate)

**NOVELTY_THRESHOLD = 0.7** — from AutoResearch idea-pipeline.

For each core claim:
1. Search arXiv: `mcp__arxiv__arxiv_search(query="<key terms from claim>", max_results=10)`
2. Compare against comparison_matrix entries.
3. Score each claim's novelty (0-1 scale, see below).
4. Dispatch a blank-context Agent for cross-model novelty assessment (Agent receives: all claims + closest prior work abstracts, ZERO conversation history).

Novelty scoring:
| Score | Criteria |
|-------|----------|
| 1.0 | No prior work claims this; verified by Agent |
| 0.7 | Prior work hints but didn't test; distinct approach |
| 0.5 | Similar idea; different methodology |
| 0.3 | Prior work tested; different dataset/domain |
| 0.0 | Prior work already demonstrated |

**Hard gate:** If any CORE claim scores < NOVELTY_THRESHOLD (0.7):
- If the claim can be adjusted to distinguish from prior work → adjust and re-score
- If the claim cannot be adjusted → flag as `weak_novelty` with blocking_issue
- If ALL core claims score < 0.7 → BLOCK the phase (the project adds nothing new)
- If some core claims pass → proceed with warnings on weak-novelty claims

If a claim overlaps with prior work, adjust it to reflect the specific difference, or flag as weak-novelty.

Write `ideas/novelty-report.md`.

### Step 7: Generate Roadmap (from idea-roadmap)

Convert the design brief and claims into a structured roadmap with Go/No-Go gates.

**ROADMAP.md** (stage convergence with tree numbering):
```markdown
# Research Roadmap: [Project Title]

## Stage 1: Baseline Establishment [Go/No-Go]
- 1.1 Implement baseline methods
- 1.2 Verify baseline correctness
- 1.3 Record baseline metrics
- **Go criteria:** All baselines run, results within expected range, 6-file contract verified
- **No-Go:** Baseline cannot be implemented or produces unreasonable results → redesign

## Stage 2: Core Claims Validation [Go/No-Go]
- 2.1 C1: [claim text] — [experiment]
- 2.2 C2: [claim text] — [experiment]
- **Go criteria:** >= 2 core claims SUPPORTED with evidence score >= 0.5
- **No-Go:** All core claims REFUTED or INCONCLUSIVE → return to Step 2 (divergent brainstorming)

## Stage 3: Ablation and Analysis [Go/No-Go]
- 3.1 Component ablation for each supported claim
- 3.2 Multi-seed statistical validation
- 3.3 Cross-claim synthesis
- **Go criteria:** Ablation confirms component contributions, >= 5 seeds per claim, statistics significant
- **No-Go:** Ablation contradicts claim → downgrade claim to PARTIAL

## Stage 4: Finalization
- 4.1 Claims Matrix v2
- 4.2 Investigation report
- 4.3 Paper writing handoff
```

**PLAN.md** (research convergence):
```markdown
# Research Plan: [Project Title]
## Research Question: [one sentence]
## Core Claims: [list C1-Cn]
## Method: [how we'll test each claim]
## Required Baselines: [list]
## Required Data/Resources: [list]
## Estimated Timeline: [per stage]
## Risk Mitigation: [per risk from register]
```

Three Go/No-Go categories:
- **Engineering Go:** Hardware resources sufficient, code compiles, baselines run
- **Research Go:** Pilot signal positive, novelty confirmed, core claims testable
- **Output Go:** Claims matrix complete, evidence >= 0.5 for core claims, paper outline ready

### Step 8: Produce Output

Write to `ideas/`:
- `design-brief.md` — accumulated 5-segment output
- `claims-matrix.md` — Claims-Evidence Matrix v1 (evidence="_pending_")
- `novelty-report.md` — cross-model novelty results
- `risk-register.md` — 3-5 risks with early-warning + mitigation

### Step 9: Self-Validate

Load `references/standards/idea-standards.md`. Check EVERY item:

Claims DAG:
- [ ] `claims-dag.yml` exists on disk? Verify: `ls ideas/claims-dag.yml`
- [ ] Every claim in the matrix has a DAG entry?
- [ ] Dependency claims reference only existing claim IDs?
- [ ] No circular dependencies (must be a valid DAG)?
- [ ] Main claims (no dependencies) are correctly identified?
- [ ] Investigation order respects DAG (main claims first, then dependents)?
If claims-dag.yml is missing → BLOCKING_ISSUE. Do not mark valid=true without it.
- [ ] RQ falsifiable?
- [ ] Causal chain described? Uncertain link annotated? Confounders listed?
- [ ] Discriminating condition exists? Missing-data plan exists?
- [ ] Primary metric justified? Baseline defined? Negative control defined?
- [ ] >= 2 testable claims? Each has: hypothesis, quantitative prediction, verification method, required baselines, falsification condition?
- [ ] Novelty verified? Difference from closest prior work stated?
- [ ] >= 3 risks? Each has early-warning + mitigation? Fatal vs delaying distinguished?

Unchecked → blocking_issues. Non-goal compliance:
- [ ] No claims address areas listed in project non_goals?
- [ ] Claims scope matches the RQ?

Return valid: true only if ALL items checked AND output files exist on disk AND non-goal compliant.
Verify with: `ls ideas/design-brief.md ideas/claims-matrix.md ideas/novelty-report.md ideas/risk-register.md`.
Missing files → blocking_issue.

### Step 10: Update State

Update `guidetree/project.yaml`:
- phases.ideas.status = "done"
- phases.ideas.valid = (true/false)
- phases.ideas.artifacts = { design_brief, claims_matrix, novelty_report, risk_register }
- If valid: set current_phase = "investigation"

## Output

- `ideas/design-brief.md`
- `ideas/claims-matrix.md` — v1 (evidence="_pending_")
- `ideas/novelty-report.md`
- `ideas/risk-register.md`

## Next Skill

After this skill: `seek:investigate`
