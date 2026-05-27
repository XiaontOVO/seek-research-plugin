# Coding Standards

> Violating any hard rule → code cannot enter the experiment phase.

## Hard Rules

### Correctness
- [ ] Every function has explicit input/output type annotations (Python: type hints, Rust: trait bounds, TypeScript: explicit types)
- [ ] Every module has at least one end-to-end test (verifying the full data path)
- [ ] Random seeds are fixed and reproducible (must explicitly record seed value in config; system-time-based seeding forbidden)
- [ ] Error paths are handled (no silent failures; errors must carry context)

### Simplicity
- [ ] Single function ≤ 50 lines (split if longer, unless it's an unavoidable configuration function)
- [ ] Single file ≤ 300 lines (split into modules if longer)
- [ ] No unnecessary abstraction (one implementation doesn't need an interface/base class/protocol)
- [ ] No copy-paste (same logic repeated 3+ times → extract a function)

### Readability
- [ ] Variable names are self-explanatory (forbidden: x, tmp, data, result, val, temp, foo, bar)
- [ ] Magic numbers have named constants (DEFAULT_LEARNING_RATE = 0.001)
- [ ] Complex logic has a one-line comment explaining WHY (not WHAT — code already says what)

### Experiment Code Rules
- [ ] All hyperparameters in a single config file (not scattered across the codebase)
- [ ] Experiment results written to structured files (JSON/CSV), not stdout print()
- [ ] Every run records: git commit hash + CLI arguments + hardware info + start/end timestamps
- [ ] Ablation controlled via config flags, not by editing source code

### Review Rules
- [ ] Changes > 20 lines → Agent code review (blank context, zero conversation history)
- [ ] New module → Agent code review + at least 1 integration test
- [ ] Review finds CRITICAL → fix and re-review (max 2 rounds)

## TDD Iron Law (from AutoResearch implement-test-driven-development)

**Iron Law: No production code without a failing test first.**

You don't know if you're testing the right thing unless you see the test fail first.
Tests that pass on first run prove nothing — they might be testing the wrong thing or never actually running.

### TDD Cycle (RED → GREEN → REFACTOR)
1. **RED:** Write a minimal failing test. Run it. Watch it fail.
2. **GREEN:** Write the minimal code to make the test pass. Run it. Watch it pass.
3. **REFACTOR:** Improve the code while keeping tests green. Remove duplication. Improve names.

### Common Excuses (and Why They're Wrong)

| Excuse | Reality |
|--------|---------|
| "This is too simple to need a test" | Simple things break in unexpected ways. A test is 5 lines. |
| "I'll add tests later" | Later never comes. Tests written after code test what you built, not what you intended. |
| "Tests slow me down" | Debugging without tests is 5-10x slower. Tests ARE speed. |
| "It's just a prototype" | Prototypes become production. Tests make prototypes into reusable components. |
| "I can't test this — it needs external resources" | Mock the external dependency. If you can't mock it, refactor until you can. |
| "The interface is still changing" | Tests guide interface design. If it's hard to test, the interface is wrong. |
| "Tests are for junior developers" | Senior developers write MORE tests because they know what breaks. |
| "I tested it manually" | Manual testing doesn't scale. You won't re-test after every change. |
| "There's no time in the deadline" | Skipping tests adds 2-3x debugging time. You're trading 10 min now for 2 hours later. |
| "Coverage is already high enough" | Coverage measures what code runs, not what's tested correctly. One good test > 10 coverage-only tests. |

### Red Flags (Stop and Restart TDD)
- [ ] Writing test after code → STOP. Delete the test (or the code). Start RED.
- [ ] Test is >20 lines for a simple function → STOP. Your function does too much.
- [ ] Test passes on first run without writing code → STOP. The test is wrong.
- [ ] Can't figure out how to test something → STOP. The interface needs refactoring.
- [ ] "I'll just test this manually" → STOP. Go back to RED.
- [ ] Mocking more than 2 dependencies → STOP. Function has too many responsibilities.
