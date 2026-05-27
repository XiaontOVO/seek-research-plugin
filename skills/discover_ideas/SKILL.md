---
name: discover_ideas
family: ideas
description: > Divergent idea discovery grounded in literature gaps. Generates 8-12 candidate ideas, filters by feasibility/novelty/impact, deep-validates survivors via devil's advocate Agent, runs pilot experiments on top 2-3, and produces a ranked list with a selected top idea. NOT for convergent design — use design_ideas. NOT for literature — use review_literature.
---

# discover_ideas

**Core principle:** Never brainstorm without literature grounding. Ideas without prior work are guesses. Kill weak ideas early — eliminating 10 bad ideas in filtering is better than implementing 1 and failing.

Phase 2a of the Seek pipeline. Divergent phase: generates many ideas from literature gaps, ruthlessly filters, pilot-validates, and selects the best one. The output (selected-idea.md) feeds into `seek:design_ideas` for convergent Socratic design.

## When To Use

Trigger phrases:
- "Find research ideas in [area]" / "what can we work on"
- "Brainstorm from the literature gaps"
- Invoked by orchestrator after Phase 1 (review_literature) completes.
- If the user already has a specific research question, skip this and go directly to `seek:design_ideas`.

## NOT For

- Sharpening a single RQ — use `seek:design_ideas`
- Literature review — use `seek:review_literature`
- Running full experiments — use `seek:investigate`

## Constants (from idea-discover)

- PILOT_MAX_HOURS = 2 — Skip pilots estimated > 2h per GPU
- PILOT_TIMEOUT_HOURS = 3 — Hard timeout per pilot
- MAX_PILOT_IDEAS = 3 — Pilot at most 3 ideas
- MAX_TOTAL_GPU_HOURS = 8 — Total GPU budget
- AUTO_PROCEED = true — If user doesn't respond at checkpoint, proceed with best option

## Output Directory Convention

```bash
mkdir -p ideas
```

## Workflow

### Step 0: Pre-Flight Checks
```bash
ls literature/comparison-matrix.md literature/gap-analysis.md 2>/dev/null && echo "LIT_OK" || echo "LIT_MISSING"
```
If LIT_MISSING → blocking_issue. Cannot discover ideas without literature foundation.

### Step 1: Load Inputs
- project_context, literature_review (comparison_matrix, gap_analysis)

### Step 2: Literature Landscape Mapping
From the comparison matrix and gap analysis:
1. Group papers by sub-direction/approach
2. Identify what has been tried and what hasn't
3. Note recurring limitations in "Future Work" sections
4. Flag open problems stated by multiple papers
5. Identify structural gaps:
   - Methods that work in domain A but untried in domain B
   - Contradictory findings between papers
   - Assumptions everyone makes but nobody tested
   - Scaling regimes unexplored

Write landscape summary to `ideas/landscape-map.md`.

### Step 3: Divergent Brainstorming

Use Agent(subagent_type="general-purpose") with ZERO conversation history to generate 8-12 concrete ideas grounded in the landscape map. For each idea:
- One-sentence summary
- Core hypothesis
- Minimum viable experiment
- Contribution type (new method / improvement / analysis / negative result / survey)
- Risk level (high / medium / low)
- Estimated GPU-hours

Write to `ideas/idea-candidates.md`.

→ CHECKPOINT: Write idea-candidates.md NOW.

### Step 4: First-Pass Filtering (eliminate ~half)

For each idea, check:
1. **Feasibility** — compute, data, implementation complexity within project constraints?
2. **Novelty quick-check** — 2-3 targeted arXiv searches. Already done?
3. **Impact** — "So what?" test. Would anyone cite this?
4. **Eliminate** ideas requiring > 1 week GPU, unavailable datasets, or novelty < 0.3

Update idea-candidates.md with filter results. Mark eliminated ideas with elimination reason.

→ CHECKPOINT: Update idea-candidates.md with filter results NOW.

### Step 5: Deep Validation (4-6 survivors)

For each surviving idea:
1. Deep novelty check via Agent(subagent_type="general-purpose") — multi-source search against arXiv, Semantic Scholar
2. Devil's advocate review: "Strongest reviewer objection? Most likely failure mode?"
3. Rank by: (novelty × impact) / risk

If Agent unavailable → perform novelty check manually with `mcp__arxiv__arxiv_search`.

### Step 6: Pilot Experiments (top 2-3 ideas, skip if no GPU)

Design minimal experiments (30 min - 2h per pilot on 1 GPU):
```bash
for idea in idea_1 idea_2 idea_3; do
    python pilot_$idea.py --timeout $((PILOT_TIMEOUT_HOURS * 3600)) &
done
wait
```
- Kill any pilot exceeding PILOT_TIMEOUT_HOURS
- Re-rank based on empirical evidence
- Track total GPU-hours against MAX_TOTAL_GPU_HOURS
- Skip pilots if purely theoretical or no GPU → document reason

Write `ideas/pilot-results.md`.

→ CHECKPOINT: Write pilot-results.md NOW.

### Step 7: Select Top Idea

Select the best idea based on: pilot signal + novelty + feasibility + impact.
Write `ideas/selected-idea.md` with:
- Selected idea title and summary
- Why it won (evidence from filtering, validation, pilots)
- Runner-up ideas (backups if top idea fails)
- Eliminated ideas with reasons
- Recommended next step: "Proceed to seek:design_ideas"

→ CHECKPOINT: Write selected-idea.md NOW.

### Step 8: Self-Validate

- [ ] Ideas grounded in literature gaps?
- [ ] 8-12 ideas generated before filtering?
- [ ] First-pass filter applied with explicit elimination reasons?
- [ ] Deep validation on >= 4 survivors?
- [ ] Devil's advocate review performed?
- [ ] Pilot attempted for top 2-3 (or documented skip reason)?
- [ ] Selected idea clearly marked with justification?
- [ ] All files exist on disk? Verify: `ls ideas/`

Return valid: true only if ALL items checked.

### Step 9: Update State

Update guidetree/project.yaml: phases.ideas.status = "done", phases.ideas.valid = true, set current_phase = "ideas" (for design_ideas follow-up).

## Output

- `ideas/landscape-map.md`
- `ideas/idea-candidates.md`
- `ideas/pilot-results.md`
- `ideas/selected-idea.md`

## Next Skill

After this skill: `seek:design_ideas`
