# Seek — AI Agent Guidelines

> **One research project, one pipeline. Load standards, execute, check. No standard, no action.**

## If You Are an AI Agent

This plugin guides research from question to paper through a fixed 8-phase pipeline. Each phase loads mandatory standards before any action. The orchestrator enforces validation gates.

**Core principles:**
- LOAD STANDARDS → EXECUTE → CHECK AGAINST STANDARDS → PASS/FAIL
- **CHECKPOINT AFTER EVERY OUTPUT FILE.** Write the file to disk immediately. Never batch writes.
- No standard, no action. No checklist, no done.
- Tag inferences with confidence (confirmed | likely | speculative).

## ★ MANDATORY CONTROL PLANE FILES (before ANY phase work)

Every phase skill MUST write these files BEFORE executing the phase. No exceptions.

```
1. guidetree/plan/stage_dags/P<N>-stage_dag.json   ← stages + dependency edges
2. guidetree/plan/steps/P<N>.S<M>-steps.json       ← one per stage, atomic steps
3. guidetree/registry/artifact_registry.json        ← register every product file
4. guidetree/state/current_state.json               ← current phase/stage/step
5. guidetree/state/execution_history.jsonl          ← append after each step
```

**Stage DAG format:**
```json
{"phase_id":"P1","stages":[{"id":"P1.S1","name":"Search","depends_on":[]},{"id":"P1.S2","name":"Triage","depends_on":["P1.S1"]}],"edges":[["P1.S1","P1.S2"]]}
```

**Step plan format:**
```json
{"stage_id":"P1.S1","steps":[{"id":"P1.S1.S1","name":"Pre-flight","action":"curl Zotero","expected_output":"search-log.md header"}]}
```

**Artifact registry format:**
```json
{"artifacts":[{"artifact_id":"ART-001","type":"literature","path":"literature/search-log.md","phase_id":"P1","stage_id":"P1.S1","step_id":"P1.S1.S1","status":"draft"}]}
```

**Empty directory shells are NOT acceptable.** Every control plane directory must contain its JSON/YAML file. If a file is missing, the phase is incomplete.

**Skipped phases** (e.g. investigate for literature_survey): Write a stage DAG with `{"phase_id":"P4","status":"skipped","reason":"literature_survey project_type — no code or experiments needed"}`. Skipped phases must still be documented.

**Execution log:** Append one JSON line to `guidetree/state/execution_history.jsonl` after EVERY step completes. Format: `{"step_id":"P1.S1.S1","status":"completed","timestamp":"...","output":"literature/search-log.md"}`. Do NOT skip logging for any step.

**DO NOT create old-style `guidetree/phase-NN-name/stages/` directories.** The control plane uses `guidetree/plan/`, `guidetree/state/`, `guidetree/registry/` — NOT per-phase directories under guidetree/.

## The Seek Research Pipeline

```
define_context     (Phase 0: Pre-flight + Socratic interview + hardware detect + Zotero check)
     ↓
review_literature  (Phase 1: Zotero-first → 5-tier fallback search → triage → deep-read → matrix)
     ↓
discover_ideas     (Phase 2a: Divergent brainstorming → 8-12 ideas → filter → pilot top 2-3)
     ↓
design_ideas       (Phase 2b: Convergent Socratic design → Claims DAG → Matrix v1 → novelty gate → roadmap)
     ↓
investigate        (Phase 3: ★ Claims-driven unified code+experiment loop, 10 atomic steps per claim)
     ↓
communicate        (Phase 4: Claims Matrix → paper plan → write → blank-context Agent review)
     ↓
audit              (Phase 5: 3-Agent parallel gate audit + claims + citations + reproducibility + Gold scoring)
     ↓
crystallize        (Phase 6: Gold mining → evidence folder → vulnerability map → meta-lessons)
     ↓
COMPLETE
```

## Standards Layer (7 Files)

Before ANY phase action, load the relevant standards file. Every checklist item is a verifiable yes/no hard constraint.

| Phase | Standards File | Pre-flight Checks |
|-------|---------------|-------------------|
| context | `context-standards.md` | Hardware detect, Zotero connectivity |
| literature | `literature-standards.md` | Zotero API + network connectivity |
| ideas | `idea-standards.md` | Literature gap analysis loaded |
| investigation | `coding-standards.md` + `experiment-standards.md` | Hardware, dependencies, disk space |
| communication | `writing-standards.md` | Claims Matrix v2 loaded |
| audit | `audit-standards.md` | Paper + data + citations available |

## Pre-Flight Pattern (Every Skill)

Before executing any phase work, run pre-flight checks:

1. **Permissions:** Can we access required APIs/tools?
2. **Dependencies:** Are required artifacts from previous phases available?
3. **Connectivity:** Can we reach external services if needed?
4. **Resources:** Enough disk space, memory, compute?

If any pre-flight fails → record as blocking_issue, stop, report to operator.

## Validation Report Format (Every Phase Output)

Every phase produces a structured validation report:
```yaml
valid: true/false
blocking_issues:
  - id: "B1"
    issue: "What's wrong"
    location: "Which artifact/section"
    reason: "Why it blocks"
    required_fix: "How to fix it"
non_blocking_warnings:
  - id: "W1"
    warning: "What's concerning"
    location: "Which artifact/section"
    suggestion: "How to address it"
repair_suggestions:
  - target: "Which artifact"
    action: "What to do"
    rationale: "Why this fixes it"
```

Blocking issues prevent phase advancement. Warnings allow advancement with caveats.
Max 3 repair attempts per phase. After 3 → phase marked `blocked`, operator input needed.

## The Orchestrator

`seek:orchestrate` is the central control skill. It:
1. Inspects `guidetree/project.yaml`
2. Determines which phases exist and are valid
3. Selects exactly ONE next skill to invoke
4. Prepares minimal input for that skill
5. Returns the decision

Selection rules are priority-ordered, first-match-wins. The orchestrator enforces:
- No phase transition without `valid: true`
- No repair without validation feedback
- Phase lock (when enabled, routes to current_phase regardless of progression)

## The Claims-Evidence Matrix (Central Artifact)

The backbone of Seek, flowing through all phases:
- **Phase 2a (discover) + 2b (design):** Matrix v1 created. Claims defined, evidence = "_pending_".
- **Phase 3 (investigation):** Matrix v2 populated. Each claim validated through the 10-step investigation loop. Evidence column filled with pointers to experiment data.
- **Phase 4 (communicate):** Matrix v2 drives paper writing. Every paper claim maps to matrix evidence.
- **Phase 5 (audit):** Matrix v2 cross-checked against raw data by blank-context Agent.

## The Investigation Loop (Phase 3) — 10 Atomic Steps Per Claim

Code and experiment are NOT separate phases. Each claim goes through:

```
1. RESTATE hypothesis (quantitative prediction + falsification condition)
2. IMPLEMENT code (ONLY for this claim, coding-standards.md enforced)
3. REVIEW code (blank-context Agent if > 20 lines or new module)
4. VALIDATE experimental design (does this test the hypothesis?)
5. SANITY CHECK (small scale, verify pipeline works, max 3 fix attempts)
6. EXECUTE experiment (>= 3 seeds, parallel for <= 5 jobs, queue for >= 6)
7. DATA QUALITY check (NaN/Inf, convergence, statistical assumptions)
8. ANALYZE results (effect size + significance + delta vs baseline)
9. DECIDE: SUPPORTED → next claim / PARTIAL → adjust, loop (max 5) / REFUTED → document
10. PERSIST state (investigation-state.json for recovery)
```

A core claim being REFUTED is a valid scientific outcome — it does NOT alone make valid=false.

## Subagent Types (All Zero Conversation History)

| Agent | When | Receives |
|-------|------|----------|
| Code Reviewer | New code > 20 lines | Code + hypothesis card + coding-standards.md |
| Novelty Verifier | After idea design | Claims + closest prior work abstracts |
| Gate Auditor (x3) | Audit phase | Structure/Rigor/Domain review (parallel) |
| Claims Auditor | Audit phase | Paper claims + raw experiment data |
| Reproducibility | Audit phase | Code + config + data + README |
| Paper Reviewer | Communication phase | Paper draft + claims matrix + writing standards |
| Statistical Analyst | Complex analysis | Raw data + analysis plan (no conclusions) |

## Output Directory Hierarchy (GuideTree Pattern)

Output has TWO layers:

**1. Control Plane (`guidetree/`)** — Agent governance: plans, state, validation, registry.
**2. Product Plane (root level)** — Actual deliverables, NOT inside guidetree/.

```
project/
├── README.md                       # Project overview
├── hardware-profile.json           # Hardware profile (from context phase)
│
├── guidetree/                      # ★ CONTROL PLANE — agent governance
│   ├── phase-00-context/
│   │   ├── phase.state.yaml
│   │   └── stages/
│   │       ├── stage-01-interview/stage.state.yaml
│   │       └── stage-02-hardware/stage.state.yaml
│   ├── phase-01-literature/
│   │   ├── phase.state.yaml
│   │   └── stages/
│   │       ├── stage-01-search/stage.state.yaml
│   │       ├── stage-02-triage/stage.state.yaml
│   │       ├── stage-03-deepread/stage.state.yaml
│   │       └── stage-04-matrix/stage.state.yaml
│   ├── phase-02-discover/.../      # brainstorm→filter→pilot (3 stages)
│   ├── phase-03-design/.../        # socratic→dag→novelty→roadmap (4 stages)
│   ├── phase-04-investigate/.../   # setup→baseline→claims→finalize (4 stages)
│   ├── phase-05-communicate/.../   # plan→write→review (3 stages)
│   ├── phase-06-audit/.../         # gate→claims→citations→reproduce (4 stages)
│   └── phase-07-crystallize/.../   # score→evidence (2 stages)
│
├── literature/                     # ★ WORK PRODUCT: literature review deliverables
│   ├── search-log.md
│   ├── paper-notes/                # one .md per deep-read paper
│   ├── comparison-matrix.md
│   └── gap-analysis.md
│
├── ideas/                          # ★ WORK PRODUCT: idea phase deliverables
│   ├── idea-candidates.md          # 8-12 candidate ideas (from discover)
│   ├── selected-idea.md            # top idea (from discover)
│   ├── design-brief.md             # 5-segment Socratic output (from design)
│   ├── claims-dag.yml              # dependency DAG (from design)
│   ├── claims-matrix.md            # Claims Matrix v1 (from design)
│   ├── novelty-report.md           # novelty verification (from design)
│   └── roadmap.md                  # Go/No-Go roadmap (from design)
│
├── src/                            # ★ WORK PRODUCT: source code
│   └── *.py, *.rs, etc.
│
├── configs/                        # ★ WORK PRODUCT: experiment configurations
│   └── *.yaml
│
├── runs/                           # ★ WORK PRODUCT: experiment data (6-file contract)
│   ├── INDEX.yml
│   └── <experiment-name>/
│       └── seed_<N>/
│           ├── raw_record.json, attempts.csv, metrics.csv
│           ├── config.yaml, hardware_info.json, summary.md
│
├── analysis/                       # ★ WORK PRODUCT: per-claim analysis
│   ├── hypothesis-cards/           # one .md per claim
│   └── analysis-notes/             # one .md per claim
│
├── paper/                          # ★ WORK PRODUCT: manuscript
│   ├── paper-plan.md
│   ├── figure-plan.md
│   ├── draft.md                    # (or draft.tex)
│   └── review-log.md
│
├── audit/                          # ★ WORK PRODUCT: audit reports
│   ├── gate-audit.md
│   ├── claims-audit.md
│   ├── citation-audit.md
│   ├── reproducibility-audit.md
│   └── final-verdict.md
│
└── gold/                           # ★ WORK PRODUCT: crystallized evidence
    ├── GOLD_MANIFEST.md
    ├── GOLD_INDEX.md
    ├── code/                       # copied source files
    ├── data/                       # key experiment records
    └── meta/                       # lessons learned, project template
```

**CRITICAL:** Every phase skill MUST:
1. Write stage DAG to `guidetree/plan/stage_dags/P<N>-stage_dag.json` BEFORE executing
2. Write step plans to `guidetree/plan/steps/P<N>.S<M>-steps.json` BEFORE executing each stage
3. Register every expected output in `guidetree/registry/artifact_registry.json` BEFORE producing it
4. Update `guidetree/project.yaml` current.phase_id/stage_id/step_id after each transition
5. Log execution to `guidetree/state/execution_history.jsonl`

Plan structure:
```
guidetree/plan/
├── stage_dags/P4-stage_dag.json    ← stages + dependency edges for Phase 4
└── steps/
    ├── P4.S1-steps.json            ← atomic steps for Setup stage
    ├── P4.S2-steps.json            ← atomic steps for Baseline stage
    ├── P4.S3-steps.json            ← atomic steps for Claims stage
    └── P4.S4-steps.json            ← atomic steps for Finalize stage
```

State tracking:
```
guidetree/project.yaml → current: { phase_id: "P4", stage_id: "P4.S2", step_id: "P4.S2.S1" }
guidetree/state/execution_history.jsonl → append after each step: { step_id, status, timestamp }
guidetree/registry/artifact_registry.json → register each output: { artifact_id, step_id, path, type, status }
```

## Plugin File Layout

```
seek/
├── .claude-plugin/          # Plugin manifest
├── hooks/                   # Session-start hook
├── references/
│   ├── standards/           # 7 standards (hard constraints)
│   ├── paths.yml            # Output hierarchy (GuideTree pattern)
│   └── templates/           # pipeline-state.yml, prompts, gate configs
├── skills/
│   ├── orchestrate/         # State machine
│   ├── define_context/      # Phase 0
│   ├── review_literature/   # Phase 1
│   ├── discover_ideas/      # Phase 2a
│   ├── design_ideas/        # Phase 2b
│   ├── investigate/         # Phase 3
│   ├── communicate/         # Phase 4
│   ├── audit/               # Phase 5
│   └── crystallize/         # Phase 6
├── scripts/
├── test/
├── CLAUDE.md / AGENTS.md / INDEX.md / README.md
```

## Key Rules

- **Standards first** — load relevant standards before any phase action.
- **Pre-flight checks** — permissions, dependencies, connectivity before execution.
- **One skill at a time** — the orchestrator selects exactly one.
- **Validate before advancing** — no phase transition without valid=true.
- **Evidence required** — every claim must trace to raw experiment data.
- **Blank-context review** — all Agent reviews receive zero conversation history.
- **Repair by re-invocation** — no separate repair skills; re-invoke same skill with feedback.
- **State is truth** — `guidetree/project.yaml` controls everything.
- **Phase lock** — when enabled, only current_phase skill may execute.
- **Confidence tags** — all inferred information tagged (confirmed | likely | speculative).
- **Max 3 repairs** — after 3 failed repair attempts, phase is blocked.

## What Not To Do

- Do NOT skip standards. Load them before every phase.
- Do NOT skip pre-flight checks. Verify tools/permissions/connectivity first.
- Do NOT skip validation gates. No phase transition without valid=true.
- Do NOT separate code and experiment. The investigation loop is ONE process.
- Do NOT make claims without evidence. The Claims Matrix is the backbone.
- Do NOT skip sanity checks. Never run full experiments without sanity first.
- Do NOT fabricate citations. Every citation must be verified.
- Do NOT treat subagent reviews as optional. Blank-context review catches what you miss.
- Do NOT use vague acceptance criteria (see acceptance-criteria-rules.md for banned phrases).
- Do NOT treat assumptions as facts. Tag all inferences with confidence level.
