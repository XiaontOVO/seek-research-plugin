---
name: define_context
family: context
description: > Research context definition. Socratic interview + hardware detection + Zotero check + prior work inheritance. Produces project_context.md that all downstream phases depend on. Invoked by orchestrator after /seeker. NOT for literature review — use review_literature. NOT for idea design — use design_ideas.
---

# define_context

**Core principle:** A research question without a falsification condition is not a question. No invented answers — vagueness surfaced, not filled in.

Phase 0 of the Seek pipeline. Understands what the user wants to research, what resources they have, and what constraints they face. Produces a normalized project_context.

## When To Use

Trigger phrases:
- "Start research on [topic]"
- "I want to investigate [research question]"
- Invoked by orchestrator when context phase is not_started or needs_repair.

## NOT For

- Literature search — use `seek:review_literature`
- Generating research ideas — use `seek:design_ideas`
- Running experiments — use `seek:investigate`

## Standards

Before any action, load `references/standards/context-standards.md`. Every checklist item is a hard constraint.

## Output Directory Convention

All paths from `references/paths.yml`. Before any work, create the output directory:

```bash
mkdir -p guidetree/context
```

## Workflow

### Step 0: Pre-Flight Checks
Before any research work, verify:
```bash
# Permissions: can we write to the output directory?
mkdir -p guidetree/context && touch guidetree/context/.write_test && rm guidetree/context/.write_test && echo "WRITE_OK" || echo "WRITE_FAILED"
# Hardware: can we detect system info?
python -c "import platform, os; print(f'OS: {platform.system()}, CPU cores: {os.cpu_count()}')"
```
If WRITE_FAILED → blocking_issue. Stop and report.

### Step 1: Detect Hardware
```bash
python d:/Research/plugin/seek/scripts/detect_hardware.py
```
If unavailable, use built-in detection:
```bash
nvidia-smi --query-gpu=name,memory.total --format=csv,noheader 2>/dev/null || echo "NO_GPU"
lscpu 2>/dev/null | head -10 || cat /proc/cpuinfo 2>/dev/null | head -10
```
Record: OS, CPU (cores), GPU (model + VRAM), RAM (GB), disk free (GB), Python version.

Write to `guidetree/context/hardware-profile.json`.

### Step 2: Check LocalLiterature
```bash
ls "D:/LocalLiterature/" 2>/dev/null | head -10 && echo "LOCALLIT_AVAILABLE" || echo "LOCALLIT_MISSING"
find "D:/LocalLiterature/" -name "*.pdf" 2>/dev/null | wc -l && echo "PDFs in library"
```
Record status: available | missing. LocalLiterature is the primary paper source.

### Step 3: Socratic Interview

Max 3 rounds per question. If unclear after 3 rounds, record best-effort with `_TODO_` and proceed.

Q1: "What is your research question in one sentence?"
Q2: "What observation would falsify your hypothesis — what counts as a 'no'?"
Q3: "What are your hard constraints?" (time, compute, data, expertise)
Q4: "Is there prior work from you/your lab to inherit from?"
Q5: "What are your explicit non-goals — things you are deliberately NOT doing?"

Do NOT invent answers. If the user is vague, surface the vagueness — don't fill it in.

### Step 4: Inherit from Prior Projects

If prior work exists, scan for:
```bash
find . -name "GOLD_MANIFEST.md" -o -name "design-brief.md" -o -name "experiment-plan.md" 2>/dev/null | head -20
```
Extract reusable assets: methods, baselines, experiment harness patterns, lessons learned.

### Step 5: Produce Output

Write `guidetree/context/project-context.md` containing:
- Research question (one sentence)
- Falsification condition (observable)
- **project_type**: `computational_experiment` | `literature_survey` — determines whether investigation phase requires code+experiments or just synthesis
- Constraints (time, compute, data)
- Non-goals (explicitly out of scope)
- Hardware profile summary
- LocalLiterature status
- Prior work inheritance (if any)
- Unanswered questions (marked `_TODO_`)
- Assumptions table (confirmed | likely | speculative)

### Step 6: Self-Validate

Load `references/standards/context-standards.md`. Check EVERY item:
- [ ] RQ stated in one sentence?
- [ ] RQ specific enough for scope?
- [ ] Falsification condition explicit, observable, non-circular?
- [ ] Constraints explicit (time, compute, data)?
- [ ] Hardware profile complete?
- [ ] LocalLiterature status recorded?
- [ ] Prior projects scanned?
- [ ] All unanswered marked `_TODO_`?
- [ ] No invented answers?
- [ ] Assumptions labeled with confidence?

Unchecked → blocking_issues. Non-goal compliance:
- [ ] Output does not include any work listed in project non_goals?
- [ ] Scope matches the RQ (not expanded into adjacent areas)?

Return valid: true only if ALL items checked AND output files exist on disk AND non-goal compliant.
Verify with: `ls guidetree/context/project-context.md guidetree/context/hardware-profile.json`.
Missing files → blocking_issue.

### Readiness Gate
After self-validation, produce a readiness assessment:
```yaml
ready_for_next_phase: true/false
confidence: 0.0-1.0
reason: "Why this phase is (not) ready for literature review"
```
Set ready_for_next_phase=true only if valid=true AND all output files verified on disk.
Set confidence based on: RQ completeness, falsification clarity, constraint specificity, hardware data quality.

### Step 7: Update State

Update `guidetree/project.yaml`:
- phases.context.status = "done"
- phases.context.valid = (true/false)
- phases.context.artifacts = { project_context, hardware_profile }
- If valid: set current_phase = "literature"

## Output

- `guidetree/context/project-context.md`
- `guidetree/context/hardware-profile.json`

## Next Skill

After this skill: `seek:review_literature`
