# Seek — Subagent Guidelines

> Subagents are launched with ZERO conversation history. Their only context is the prompt they receive.

## Subagent Types and Their Roles

### 1. Code Reviewer Agent
**When:** investigation phase Step 3.3.N.3 (code changes > 20 lines or new module).
**Receives:** code diff + hypothesis card + coding-standards.md.
**Must NOT receive:** conversation history, design brief, claims matrix, experiment results.
**Output:** Review report with issues tagged CRITICAL / MAJOR / MINOR.
**Rules:**
- Check correctness: does code implement the hypothesis?
- Check coding-standards: every hard rule verified.
- Check reproducibility: fixed seeds, config-driven, structured output.
- CRITICAL → fix and re-review (max 2 rounds).

### 2. Novelty Verification Agent
**When:** design_ideas phase (cross-model novelty assessment).
**Receives:** all claims + closest prior work abstracts.
**Must NOT receive:** design brief, conversation history, author's own novelty assessment.
**Output:** Per-claim novelty assessment (novel / overlapping / prior-established).
**Rules:**
- Compare each claim against prior work abstracts.
- Flag claims that are already established.
- Suggest adjustments for borderline cases.

### 3. Gate Audit Agents (3 parallel)
**When:** audit phase (gate audit).
**Receives (Agent A — Structure):** paper draft + claims_matrix_v2.
**Receives (Agent B — Rigor):** paper draft + experiment data paths.
**Receives (Agent C — Domain):** paper draft + comparison matrix from Phase 1.
**Rules:**
- ALL Agents receive ZERO conversation history.
- Each Agent scores 0-10 on their dimension.
- Specific issues only (not "could be better" — say exactly what and where).
- JSON output format required.

### 4. Claims Audit Agent
**When:** audit phase (claims verification).
**Receives:** ALL quantitative claims from paper + ALL raw experiment data files.
**Must NOT receive:** summaries, interpretations, analysis reports, conversation history.
**Output:** Per-claim verification with 7 failure modes checked.
**Rules:**
- Only raw data files (raw_record.json, metrics.csv) — no summaries.
- Check all 7 failure modes for each claim.
- Rounding rule: only standard rounding to displayed precision is OK.
- Cross-model: different model family from executor.

### 5. Reproducibility Agent
**When:** audit phase (reproducibility audit).
**Receives:** code + config + data + README (the reproduction kit).
**Must NOT receive:** paper, claims matrix, expected results, conversation history.
**Output:** "I ran [command]. I observed [results]. This matches/does not match [paper value]."
**Rules:**
- Follow README exactly.
- Report what actually happened (not what should have happened).
- If errors prevent reproduction, report exact error messages.

### 6. Paper Review Agent
**When:** communicate phase (internal review rounds).
**Receives:** paper draft + claims_matrix_v2 + writing-standards.md.
**Must NOT receive:** conversation history, author's self-assessment.
**Output:** Score 0-10 + CRITICAL/MAJOR/MINOR issues.
**Rules:**
- Fresh Agent each round (no memory of prior reviews).
- Score ≥ 6/10 or verdict "accept" → stop review cycle.
- Max 4 rounds.

### 7. Statistical Analysis Agent
**When:** investigation phase (complex multi-condition analysis).
**Receives:** raw experiment data + analysis plan.
**Must NOT receive:** executor's preliminary conclusions.
**Output:** Independent statistical verification.
**Rules:**
- Verify: effect size computation, significance test choice, outlier handling.
- Flag errors in statistical reasoning.
- Do NOT receive executor's conclusions.

## General Subagent Rules

1. **ALL subagents receive ZERO conversation history.** Their only context is the prompt.
2. **Read-only access** to the files they receive. Never modify project files.
3. **Specific output** — no vague assessments. Every issue must cite exact location and content.
4. **JSON output when specified** — structured output for automated parsing.
5. **Cross-model preference** — where stated, reviewer should be a different model family from executor.
6. **Advisory, not blocking** — subagents flag issues; the phase skill decides.
