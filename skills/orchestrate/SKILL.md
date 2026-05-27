---
name: orchestrate
family: orchestration
description: > Central state machine for the Seek research pipeline. Inspects guidetree/project.yaml, determines the single correct next skill to invoke, and enforces all validation gates. Never performs research work directly. Invoked by /seeker or "continue research".
---

# orchestrate

**Core principle:** One skill at a time. No gate, no advance. The orchestrator decides — it never does.

**MANDATORY: Before executing any phase, the phase skill MUST write control plane files to guidetree/plan/, guidetree/state/, and guidetree/registry/. Empty directory shells are NOT valid phase output. See CLAUDE.md for required file formats.**

**CHECKPOINT RULE (applies to ALL phases):** After EVERY step that produces a file, write it to disk IMMEDIATELY. Never batch writes at the end of a phase. If interrupted, resume by checking which files exist and skipping completed steps. Progress is measured by files on disk, not by memory.

**PIPELINE STATE WARNING:** The guidetree/project.yaml may be reverted by external tools (linters, formatters). Always verify the file content after writing. If reverted, re-write ALL phase statuses from memory. Consider backing up: `cp guidetree/project.yaml guidetree/project.yaml.bak` after each phase update.

Central control for the Seek research pipeline. Reads `guidetree/project.yaml`, determines which phases exist and are valid, selects exactly ONE next skill, prepares minimal input for it, and returns the decision. Enforces all 6 validation gates. Handles repair (re-route to same phase, max 3 attempts), dead states (failed/skipped), auto-mode exhaustion, and phase_lock enforcement.

## When To Use

Trigger phrases:
- `/seeker` — enter the pipeline
- "continue research" / "continue" — resume from current state
- Invoked automatically by the runtime loop after each phase skill completes.

The orchestrator never performs project work. It only decides and delegates.

## NOT For

- Doing any research work directly (that's what phase skills are for)
- Skipping validation gates
- Generating project artifacts

## Pipeline Order (Fixed)

```
define_context → review_literature → discover_ideas → design_ideas → investigate → communicate → audit → crystallize
```

Each phase must be `status: done` AND `valid: true` before the next can be selected.

## State Detection Rules

From `pipeline_state.phases`:

```
has_X: true when phases.X.status is "done" and phases.X.valid is true
X_in_progress: true when phases.X.status is "in_progress"
X_needs_repair: true when phases.X.status is "done" and valid is false and repair_count < 3
blocker_exists: true when any phase has status "blocked" or repair_count >= 3
phase_failed: true when any phase has status "failed"
phase_skipped: true when any phase has status "skipped"
auto_mode_repairs_exhausted: true when auto_mode AND any phase repair_count >= 3 AND status "done" AND valid false
current_phase_mismatch: true when phase_lock AND first non-done-or-invalid phase != current_phase
```

## Selection Rules (Evaluated in Order — First Match Wins)

1. **phase_failed** → decision: stop_failed. Pipeline cannot continue. Operator must reset or skip the phase.
2. **auto_mode_repairs_exhausted** → decision: stop_for_blocker. Exiting auto-mode for operator.
3. **phase_skipped** → advance to next non-skipped, non-done phase.
4. **phase_lock AND current_phase_mismatch** → route to skill matching current_phase (lock override).
5. **crystallize done and valid** → decision: stop_completed.
6. **audit done and valid AND crystallize not_started** → select `seek:crystallize`
7. **blocker_exists AND not auto_mode** → decision: stop_for_blocker.
8. **a phase needs_repair** → re-route to same phase skill with repair_mode=true.
9. **a phase is in_progress** → re-select same phase skill.
10. **Phase progression** (first phase not done/valid):
   - `!has_context` → `seek:define_context`
   - `!has_literature` → `seek:review_literature`
   - `!has_discover` → `seek:discover_ideas`
   - `!has_design` → `seek:design_ideas`
   - `!has_investigation` → `seek:investigate`
   - `!has_communication` → `seek:communicate`
   - `!has_audit` → `seek:audit`
11. **No valid action** → decision: request_clarification.

## Validation Gates (Hard — Never Violate)

1. No literature review before context is done and valid.
2. No idea design before literature review is done and valid.
3. No investigation before ideas are done and valid.
4. No paper before investigation is done and valid.
5. No audit before communication is done and valid.
6. No completion before audit passes.

## Repair Strategy

When a phase returns `valid: false`:
1. Increment that phase's repair_count.
2. If repair_count < 3: set status to "in_progress", re-select same phase skill with `repair_mode: true`.
3. If repair_count >= 3: set status to "blocked" in guidetree/project.yaml, stop for operator.

The orchestrator MUST write `status: blocked` before returning stop_for_blocker.

## Skill Input Construction (Minimal)

```
seek:define_context → operator_message, hardware_profile (if pre-detected)
seek:review_literature → project_context (from context phase artifacts)
seek:design_ideas → project_context, literature_review (comparison_matrix, gap_analysis)
seek:investigate → project_context, design_brief, claims_matrix (v1, evidence "_pending_")
seek:communicate → project_context, claims_matrix_v2, investigation_report, investigation_state
seek:audit → project_context, paper_draft, claims_matrix_v2, experiment_data_paths
```

## Next Skill

After orchestrate: the skill named in `selected_skill`. The runtime loop invokes it, persists the result, then invokes orchestrate again.
