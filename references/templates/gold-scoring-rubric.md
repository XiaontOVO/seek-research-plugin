# Gold Scoring Rubric

> Adapted from AutoResearch gold skill. Used by audit and crystallize phases.

## Formula

```
gold_score = evidence_score × 0.35 + code_score × 0.25 + novelty_score × 0.25 + significance_score × 0.15
```

## Evidence Score (0-1, weight 0.35)

| Score | Criteria |
|-------|----------|
| 1.0 | Exact metric found in raw_record.json, matches claim value |
| 0.7 | Metric exists but column/field name differs |
| 0.5 | Experiment exists but specific metric needs extraction |
| 0.3 | Experiment planned but not run (simulation-only, qualitative-only) |
| 0.0 | No experiment linked to this claim |

## Code Score (0-1, weight 0.25)

| Score | Criteria |
|-------|----------|
| 1.0 | Exact file + line numbers, entrypoint verified, runs independently |
| 0.7 | Files found, approximate location, requires minor adaptation |
| 0.5 | Code exists but scattered across modules, requires significant work to run |
| 0.0 | No implementation found |

## Novelty Score (0-1, weight 0.25)

| Score | Criteria |
|-------|----------|
| 1.0 | No prior work claims this; verified by cross-model Agent |
| 0.7 | Prior work hints but didn't test; distinct approach |
| 0.5 | Similar idea; different methodology or dataset |
| 0.3 | Prior work tested; different dataset only |
| 0.0 | Prior work already demonstrated |

## Significance Score (0-1, weight 0.15)

| Score | Criteria |
|-------|----------|
| 1.0 | Field-changing (new capability, paradigm shift) |
| 0.7 | Strong (beats SOTA by meaningful margin, >= 15% improvement) |
| 0.5 | Solid (beats strong baselines, 5-15% improvement) |
| 0.3 | Incremental (beats weak baselines, < 5% improvement) |
| 0.0 | Negative result or no improvement over any baseline |

## Classification

| Tier | Score | Meaning |
|------|-------|---------|
| **GOLD** | >= 0.75 | Rock-solid. Evidence + code + novelty all strong. Ready for submission. |
| **SILVER** | >= 0.50 | Good contribution with identified gaps. Needs strengthening. |
| **BRONZE** | >= 0.30 | Preliminary. Needs more experimental work. |
| **ASPIRATION** | < 0.30 | Claim without backing. Remove from paper or downgrade to speculation. |

## Rules

- Max 3 GOLD per project. More than 3 means you're not selective enough.
- Every GOLD must trace to: experiment run + source file + line number.
- Zero-GOLD projects must prominently flag this in final verdict.
- Negative results (REFUTED claims) with strong evidence can score SILVER (evidence=1.0, significance=0.0 → 0.60).
- Simulation-only evidence caps evidence_score at 0.3.
