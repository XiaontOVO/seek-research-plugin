---
name: audit
family: audit
description: > Final safety net before submission. 3-Agent parallel gate audit + claim-by-claim evidence verification + 3-layer citation audit + independent reproducibility attempt. Advisory, never blocking — but FAIL verdicts prominently flagged. Invoked by orchestrator after communication completes. NOT for experiment auditing — that's part of investigate self-validation.
---

# audit

**Core principle:** No artifact passes without independent verification. Three fresh eyes, zero shared context. Every number traced to raw data. Every citation traced to reality. **Gates are BLOCKING — FAIL means the pipeline cannot proceed to crystallize.**

Phase 6 of the Seek pipeline. The final safety net with strict gate enforcement. FAIL blocks pipeline completion. Auto-mode: repair → re-audit (max 3 rounds) → redo phase → exit auto-mode.

## When To Use

Trigger phrases:
- "Audit the paper" / "verify the manuscript"
- "Check claims against data" / "verify citations"
- Invoked by orchestrator after Phase 4 (communicate) completes.

## NOT For

- Experiment integrity checks during investigation — the investigate self-validation handles that
- Literature review — use `seek:review_literature`
- Paper writing — use `seek:communicate`

## Standards

Before any action, load `references/standards/audit-standards.md`. Every checklist item is a hard constraint.

## Output Directory Convention

All paths from `references/paths.yml`. Before any work, create the output directory:

```bash
mkdir -p audit
```

## Workflow

### Step 0: Pre-Flight Checks
Verify all auditable artifacts exist:
```bash
ls paper/draft/*.md paper/draft/*.tex 2>/dev/null && echo "PAPER_OK" || echo "PAPER_MISSING"
ls analysis/claims-matrix-v2.md 2>/dev/null && echo "MATRIX_OK" || echo "MATRIX_MISSING"
find analysis/runs/ -name "raw_record.json" | head -5 2>/dev/null && echo "DATA_OK" || echo "DATA_MISSING"
```
If PAPER_MISSING or MATRIX_MISSING → blocking_issue. Cannot audit without these.

### Step 1: Load Inputs
- project_context
- paper_draft (all .tex/.md files)
- claims_matrix_v2
- experiment_data_paths (paths to raw_record.json, metrics.csv, etc.)
- If repair: validation_feedback

### Step 2: Gate Audit (3-Agent Parallel Review — ported from AutoResearch audit-gate)

**Step 2a: Load Gate Configuration**
Read `references/gate-configs.yml`. Extract gate_5_audit:
- name, phase_dir, threshold (7.0), artifacts[], domain_dimensions[]

**Step 2b: Verify Artifacts Exist**
```bash
ls audit/gate-audit.md audit/claims-audit.md audit/citation-audit.md audit/reproducibility-audit.md audit/final-verdict.md 2>/dev/null
```
If required artifacts missing → BLOCKED. Report what's missing, do not dispatch Agents.

**Step 2c: Load Prompt Templates**
Read from `references/prompts/`:
- `structural-review.md` — substitute {{ARTIFACT_PATHS}} with actual file paths
- `rigor-review.md` — substitute {{ARTIFACT_PATHS}} with actual file paths
- `domain-review.md` — substitute {{ARTIFACT_PATHS}} and {{DOMAIN_DIMENSIONS}} with gate config values

Resolve all artifact paths to ABSOLUTE paths before sending to Agents.

**Step 2d: Dispatch 3 Agents in PARALLEL**
All 3 run as `Agent(subagent_type="general-purpose")` with ZERO conversation history:
```
Agent A ← structural-review.md (with paths substituted)
Agent B ← rigor-review.md (with paths substituted)
Agent C ← domain-review.md (with paths + domain dimensions substituted)
```
Each Agent returns a JSON object. Parse each one.

**Step 2e: Handle Agent Failures**
- 1 Agent fails → mark dimension as `error`, compute: `total = agent_X × 0.5 + agent_Y × 0.5`
- 2+ Agents fail → BLOCKED. Pause, report. Do NOT auto-proceed.
- JSON malformed → treat as Agent failure.

**Step 2f: Compute Aggregate Score**
```
total = A.structural_score × 0.3 + B.rigor_score × 0.3 + C.domain_score × 0.4
threshold = gate_5_audit.threshold (7.0)
PASS: total >= threshold AND min(A,B,C) >= 3
WARN: total >= 5.0, < threshold
FAIL: total < 5.0 OR min(A,B,C) < 2
```

**Step 2g: Act on Result**
- PASS → proceed to claims audit. Log score.
- WARN → note warnings, proceed with caution.
- FAIL → fix issues, re-audit (max 3 rounds). After 3 FAILs → mark phase blocked.

If Agent dispatch unavailable: perform manual structured review (same 3 dimensions, same scoring) and flag as non_blocking_warning ("Manual review — Agent dispatch unavailable. Review is not independent.").

**Gate is BLOCKING.** If FAIL → fix issues → re-audit (max 3 rounds). After 3 FAILs → mark phase blocked. Auto-mode: after 3 repair rounds → redo the weakest preceding phase → re-audit.

Write `audit/gate-audit.md`.

### Step 3: Claims Audit (Number Verification)

Extract EVERY quantitative claim from the paper. For each: location, claim text, claimed value.

Cross-check against raw experiment data (raw_record.json, metrics.csv). Check 7 failure modes:
1. Number inflation (paper > raw data by more than rounding)
2. Best-seed cherry-pick (reports max, not mean ± std)
3. Config mismatch (compared methods used different settings)
4. Aggregation error (claims N seeds but ran fewer)
5. Delta error (percentage calculation differs)
6. Caption-table mismatch
7. Scope overclaim

Dispatch blank-context Agent with ALL claims + ALL raw data files (ZERO summaries, ZERO interpretations). Agent returns per-claim verification.

Verdict: all match → PASS. Rounding drift only → WARN. Any material mismatch → FAIL.

Write `audit/claims-audit.md`.

### Step 4: Citation Audit (3-Layer)

**Layer 1 — Existence:** Verify every cited paper. Priority order:
1. `mcp__arxiv__arxiv_get_metadata(paper_ids=[...])` — fastest, covers arXiv papers
2. `mcp__paperplain__fetch_paper(paper_id="DOI")` — covers DOI/published papers
3. **FALLBACK (when APIs down):** `WebSearch(query="<paper title> arXiv")` or `curl -s "https://api.crossref.org/works?query=<title>"` to verify existence. NEVER leave a citation as unverified without trying all fallback methods. Mark as `@confidence: likely` ONLY after exhausting all fallbacks.

**Layer 2 — Metadata:** Author, title, year, venue correct against canonical source.
**Layer 3 — Context:** Cited content actually supports the claim being made.

Batch verify in groups of 10-15. Mark any citation that fails any layer as `[VERIFY]` or `[REMOVE]`.

Write `audit/citation-audit.md`.

### Step 5: Reproducibility Audit

Prepare reproduction kit: code + config + data + README.
Dispatch blank-context Agent with kit ONLY (no paper, no claims matrix, no expected results).
Agent runs core experiment, reports what it observed.
Compare Agent results with paper-reported results.

Write `audit/reproducibility-audit.md`.

### Step 6: Produce Output

Write to `audit/`:
- `gate-audit.md`
- `claims-audit.md`
- `citation-audit.md`
- `reproducibility-audit.md`
- `final-verdict.md` — overall PASS | WARN | FAIL

### Step 7: Gold Score Evaluation

For each supported claim in the Claims Matrix, compute a Gold Score using the AutoResearch formula:

```
gold_score = evidence_score × 0.35 + code_score × 0.25 + novelty_score × 0.25 + significance_score × 0.15
```

**Evidence Score (0-1):**
| Score | Criteria |
|-------|----------|
| 1.0 | Exact metric found in raw_record.json, matches claim value |
| 0.7 | Metric exists but column/field name differs |
| 0.5 | Experiment exists but specific metric needs extraction |
| 0.3 | Experiment planned but not run |
| 0.0 | No experiment linked to this claim |

**Code Score (0-1):**
| Score | Criteria |
|-------|----------|
| 1.0 | Exact file + line numbers, entrypoint verified |
| 0.7 | Files found, approximate location |
| 0.5 | Code exists but scattered across modules |
| 0.0 | No implementation found |

**Novelty Score (0-1):**
| Score | Criteria |
|-------|----------|
| 1.0 | No prior work claims this; verified by cross-model Agent |
| 0.7 | Prior work hints but didn't test |
| 0.5 | Similar idea; different methodology |
| 0.3 | Prior work tested; different dataset |
| 0.0 | Prior work already demonstrated |

**Significance Score (0-1):**
| Score | Criteria |
|-------|----------|
| 1.0 | Field-changing (new capability, paradigm shift) |
| 0.7 | Strong (beats SOTA by meaningful margin) |
| 0.5 | Solid (beats strong baselines) |
| 0.3 | Incremental (beats weak baselines) |
| 0.0 | Negative result or no improvement |

**Classification:**
- **GOLD** (score >= 0.75): Rock-solid. Evidence + code + novelty all strong.
- **SILVER** (score >= 0.5): Good contribution with identified gaps.
- **BRONZE** (score >= 0.3): Preliminary. Needs more work.
- **ASPIRATION** (score < 0.3): Claim without backing.

Max 3 GOLD per project. More than 3 means you're not selective enough.

Each Gold/Silver claim must trace to: experiment run + source file + line number.

**Zero-GOLD Warning:** If the project has ZERO GOLD claims (all SILVER or below), prominently flag this. A project with no GOLD claims has no rock-solid contribution — the investigation was insufficient or claims need sharpening. This is a non_blocking_warning that MUST appear in the final verdict summary.

**Zero-Code Warning:** If ALL claims have code_score=0.0 and the project_type is `computational_experiment`, this is a BLOCKING_ISSUE. The investigation phase should have produced source code and experiment data. Analytical claims without code or experiments are only acceptable for `literature_survey` project types. If the project IS a survey, the project_type must be set correctly in define_context.

### Step 8: Adversarial Review (Optional — from audit-kill)

For high-stakes papers, run an adversarial review to stress-test the weakest claims:

**Agent 1 — Attacker:** Write the strongest possible ~200-word rejection memo.
Attack axes:
1. Theorem validity: Are there logical gaps in the argument?
2. Hypothesis-claim mismatch: Does the evidence actually prove the claim?
3. Missing proof obligations: Are there unverified assumptions?
4. Edge-case ambiguity: Does the method fail on boundary conditions?
5. Claim-evidence gap: Do the numbers actually support the conclusion?
6. Scope overclaim: Are generalization claims supported by the evidence breadth?

Attack output: Single coherent argument <= 250 words, citing specific file:line locations.

**Agent 2 — Adjudicator:** Decompose the attack into 3-7 atomic points.
For each point, classify as:
- `already_addressed` — existing text answers this
- `partially_addressed` — partially covered, needs strengthening
- `unresolved` — genuine gap that must be fixed

Adjudication is by per-point counting, NOT by the adjudicator's overall judgment.
If >= 2 points are `unresolved` → adversarial review FAILED → return to communication phase to address.

Write results to `audit/adversarial-review.md` (if run).

If Agent dispatch unavailable → skip adversarial review, note as non_blocking_warning.
Adversarial review is ADVISORY, never blocking.

### Step 9: Plugin Improvement Report

After all audits complete, write `audit/plugin-improvements.md` with concrete suggestions for improving the Seek plugin itself:

```markdown
# Plugin Improvement Report
## What worked well
- [list specific skills/mechanisms that produced good results]

## What caused friction
- [list specific issues encountered — missing instructions, unclear steps, gaps]

## Suggested fixes
| Issue | Affected Skill | Suggested Fix |
|-------|---------------|---------------|
| [specific problem] | [skill name] | [concrete fix] |

## Missing mechanisms
- [list patterns from AutoResearch/GuideTree still not absorbed]

## Quality assessment
- [honest assessment of whether the plugin produced a "serious result"]
```

If the project has ZERO GOLD claims or all BRONZE, the improvement report MUST flag this as a plugin design issue: "The pipeline produced no rock-solid contributions — the skills may need stronger enforcement of code/experiment execution."

### Step 10: Self-Validate

Load `references/standards/audit-standards.md`. Check EVERY item:
- [ ] Gate Audit: 3 Agents parallel? Total >= 6.5? Each >= 3?
- [ ] Claims Audit: Every quantitative claim extracted? Cross-checked? 7 modes checked?
- [ ] Citation Audit: Layer 1 (existence) pass? Layer 2 (metadata) pass? Layer 3 (context) pass?
- [ ] Reproducibility: Independent Agent attempted? Results match paper?

Final verdict:
- [ ] Gate Audit: PASS (>= 6.5)?
- [ ] Claims Audit: PASS or WARN (no FAIL)?
- [ ] Citation Audit: PASS (no fabricated citations)?
- [ ] Reproducibility: PASS?

Non-goal compliance:
- [ ] Audited claims do not extend beyond project scope?
- [ ] Citations are within relevant domains?

Return valid: true only if Gate PASS, Claims not FAIL, Citation PASS, Reproducibility PASS, non-goal compliant, AND output files exist on disk.
Verify with:
```bash
ls audit/gate-audit.md audit/claims-audit.md audit/citation-audit.md audit/reproducibility-audit.md audit/final-verdict.md 2>/dev/null || echo "MISSING_FILES"
```
Missing files → blocking_issue.

### Step 11: Update State

Update `guidetree/project.yaml`:
- phases.audit.status = "done"
- phases.audit.valid = (true/false)
- phases.audit.artifacts = { gate_audit, claims_audit, citation_audit, reproducibility_audit, final_verdict }
- If valid: pipeline is COMPLETE.

## Output

- `audit/gate-audit.md`
- `audit/claims-audit.md`
- `audit/citation-audit.md`
- `audit/reproducibility-audit.md`
- `audit/final-verdict.md`

## Next Skill

After this skill: none. Pipeline complete.
