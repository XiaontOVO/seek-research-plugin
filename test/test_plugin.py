#!/usr/bin/env python3
import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
ERR = []
def check(cond, msg):
    if not cond: ERR.append(msg); print(f"  FAIL: {msg}")
SKILLS = ["orchestrate","define_context","review_literature","discover_ideas","design_ideas","investigate","communicate","audit","crystallize"]
for s in SKILLS:
    check((ROOT/f"skills/{s}/SKILL.md").exists(), f"Skill {s}: SKILL.md")
    check((ROOT/f"skills/{s}/SCHEMA.md").exists(), f"Skill {s}: SCHEMA.md")
for s in ["context-standards","literature-standards","idea-standards","coding-standards","experiment-standards","writing-standards","audit-standards"]:
    check((ROOT/f"references/standards/{s}.md").exists(), f"Standard: {s}")
check((ROOT/"references/gate-configs.yml").exists(), "Gate configs")
check((ROOT/"CLAUDE.md").exists(), "CLAUDE.md")
check((ROOT/"skills/orchestrate/SKILL.md").read_text(encoding="utf-8").count("discover_ideas")>=2, "Orchestrator: discover_ideas")
check((ROOT/"skills/audit/SKILL.md").read_text(encoding="utf-8").find("BLOCKING")>-1, "Audit: blocking gate")
check((ROOT/"skills/audit/SKILL.md").read_text(encoding="utf-8").find("Plugin Improvement")>-1, "Audit: plugin improvement report")
print(f"\n{'ALL PASSED' if not ERR else f'{len(ERR)} FAILURES'}")
sys.exit(1 if ERR else 0)
