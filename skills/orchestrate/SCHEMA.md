# Self-Check Schema — orchestrate

## Input (what you need before running)
- [ ] guidetree/project.yaml loaded and parsed
- [ ] All phase statuses read (context, literature, ideas, investigation, communication, audit, crystallize)
- [ ] current_phase and phase_lock values known

## Output (what you must produce)
- [ ] **decision**: one of `invoke_skill | stop_completed | stop_for_blocker | stop_failed | request_clarification`
- [ ] **reason**: one sentence explaining why this decision
- [ ] **selected_skill**: (if invoke_skill) which skill to invoke next, e.g. `seek:review_literature`
- [ ] **selected_skill_input**: (if invoke_skill) minimal input object for that skill — project_context, prior artifacts, repair_mode flag
- [ ] **blocking_issues**: (if stop_for_blocker) list of {phase, issue, required_fix}

## Self-Check
- [ ] Did I check ALL phases in order before deciding?
- [ ] Did I enforce: no phase transition without prior phase valid=true?
- [ ] If repair needed: did I set repair_mode=true and include validation_feedback?
- [ ] If phase needs_repair and repair_count >= 3: did I mark status=blocked?
- [ ] Did I only select ONE skill?
