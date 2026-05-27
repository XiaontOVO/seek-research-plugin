---
name: crystallize
family: meta
description: > Post-pipeline gold mining. Extracts core contributions from the completed project, scores them with the Gold formula (evidence×0.35 + code×0.25 + novelty×0.25 + significance×0.15), builds a self-contained evidence folder, and produces GOLD_MANIFEST.md with vulnerability map and meta-lessons. Invoked after audit completes. NOT for during-pipeline work — the pipeline must be COMPLETE first.
---

# crystallize

**Core principle:** Every research project has 1-3 golden contributions. Find them, prove them, trace them to code and data. If you can't trace a claim to data and code, it's not gold — it's aspiration. Max 3 GOLD — more means you're not selective enough.

Post-pipeline gold mining skill. Scans the completed project (context, claims matrix, experiment data, audit results) to extract, score, and package core contributions into a self-contained evidence folder.

## When To Use

Trigger phrases:
- "What's the gold in this project?" / "extract contributions"
- "Mine the project" / "crystallize the findings"
- "What did we actually prove?"
- Invoked manually after the pipeline reaches COMPLETE.

## NOT For

- During-pipeline evaluation — the pipeline must be COMPLETE first
- Literature review — use `seek:review_literature`
- Claims verification — audit phase handles that

## Constants

- **MAX_GOLD_ITEMS = 3** — More than 3 means nothing is truly golden.
- **MIN_EVIDENCE_SCORE = 0.5** — Claims below are flagged as ASPIRATION.
- **TRACEABILITY_REQUIRED = true** — Every gold claim must trace to experiment run + source file.

## Output Directory Convention

```bash
mkdir -p gold/{code,data,meta}
```

## Workflow

### Step 1: Ingest All Data

Aggregate experiment data with Python (NOT grep — JSON is structured, exploit that):
```python
import json, glob, os
from collections import defaultdict
from statistics import mean, stdev

base = 'analysis/runs'
all_records = []
for f in glob.glob(os.path.join(base, '**', 'raw_record.json'), recursive=True):
    r = json.load(open(f))
    r['_source'] = f
    all_records.append(r)
print(f"Loaded {len(all_records)} experiment records")
```

Also read: project-context.md, claims-matrix-v2.md, investigation-report.md, gate-audit.md, claims-audit.md.

### Step 2: Extract Claims from Final Outputs

From claims-matrix-v2.md (supported claims), investigation-report.md (key findings), and the paper draft (contribution statements), extract every quantitative and qualitative claim. Record each as:
```yaml
- claim_id: "C1"
  text: "Recursive proofs reduce gas cost by 15-150x"
  source: "claims-matrix-v2.md + investigation-report.md"
  type: result
  claimed_magnitude: "15-150x"
```

### Step 3: Trace Claims to Experiment Data

For each claim, extract matching metrics from aggregated Python data. Score traceability:
| Score | Criteria |
|-------|----------|
| 1.0 | Exact metric found in aggregated data, matches claim |
| 0.7 | Metric exists but column/field name differs |
| 0.5 | Experiment exists but specific metric needs extraction |
| 0.3 | Experiment planned but not run |
| 0.0 | No experiment linked |

### Step 4: Trace Claims to Source Code

For each claim, find exact file + line ranges:
```yaml
code:
  files:
    - "src/gas_model.py:45-78"  # Verifier gas cost calculation
    - "src/experiments.py:120-155"  # Experiment runner
```
Score code availability:
| Score | Criteria |
|-------|----------|
| 1.0 | Exact file + line numbers, entrypoint verified |
| 0.7 | Files found, approximate location |
| 0.5 | Code exists but scattered |
| 0.0 | No implementation found |

### Step 5: Assess Originality

Against prior work from the comparison matrix (Phase 1) and novelty report (Phase 2):
| Score | Criteria |
|-------|----------|
| 1.0 | No prior work claims this; verified |
| 0.7 | Prior work hints but didn't test |
| 0.5 | Similar idea; different methodology |
| 0.3 | Prior work tested; different dataset |
| 0.0 | Prior work already demonstrated |

### Step 6: Compute Gold Score

```
gold_score = evidence_score × 0.35 + code_score × 0.25 + originality_score × 0.25 + significance_score × 0.15
```

Significance score:
| Score | Criteria |
|-------|----------|
| 1.0 | Field-changing (new capability, paradigm shift) |
| 0.7 | Strong (beats SOTA by meaningful margin) |
| 0.5 | Solid (beats strong baselines) |
| 0.3 | Incremental (beats weak baselines) |
| 0.0 | Negative result or no improvement |

Classification:
- **GOLD** (>= 0.75): Rock-solid. Evidence + code + novelty all strong.
- **SILVER** (>= 0.5): Good contribution with gaps.
- **BRONZE** (>= 0.3): Preliminary. Needs more work.
- **ASPIRATION** (< 0.3): Claim without backing. Remove or downgrade.

### Step 7: Build Evidence Folder

Self-contained folder — zippable and reviewable independently:
```
gold/
├── GOLD_MANIFEST.md        # English manifest (executive summary, per-item scores, vulnerability map)
├── GOLD_INDEX.md            # Claim → file:line mapping
├── code/                    # All referenced source files (copied)
├── data/                    # Key experiment records + experiment-summary.json
└── meta/                    # hardware-profile, audit reports, lessons-learned
```

Rules for gold/ folder:
- Every file referenced in manifest MUST be inside gold/
- No symlinks — copy actual files
- At least one experiment record per claim
- Folder must be zippable and reviewable independently

### Step 8: Write Meta-Lessons

Document what was learned beyond the gold claims:
1. **Audit methodology** — bugs found, symptoms, root causes
2. **Experiment harness patterns** — what worked, key design decisions
3. **Architecture Decision Records** — what was chosen, what was rejected, why
4. **Lessons learned** — "If we did it again..."
5. **Template for next project** — checklist for future research

### Step 9: Present Summary

```
## Gold Mining Complete

**Project:** <title>
**Gold:** <N> items (max 3)
**Silver:** <M> items

### GOLD (score >= 0.75)
1. <title> (0.XX) — <one-line claim>

### Vulnerability Map
- Strongest: <title>
- Weakest: <title> — <reason>
- Most at risk in rebuttal: <title>

Self-contained evidence: gold/ (NN files)
```

## Output

- `gold/GOLD_MANIFEST.md` — English manifest with scores and vulnerability map
- `gold/GOLD_INDEX.md` — Evidence index with line numbers
- `gold/code/` — All referenced source files
- `gold/data/` — Experiment evidence (summary + key records)
- `gold/meta/` — Lessons learned, audit summary, project template

## Next Skill

After crystallize: none. This is the final project artifact.
