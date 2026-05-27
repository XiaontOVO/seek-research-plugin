#!/usr/bin/env python3
"""Seek plugin integrity verification — adapted from AutoResearch verify_plugin.py"""

import json
import sys
from pathlib import Path

PLUGIN_ROOT = Path(__file__).resolve().parent.parent
ERRORS = []

def check(cond, msg):
    if not cond:
        ERRORS.append(msg)
        print(f"  FAIL: {msg}")
    else:
        print(f"  OK: {msg}")

def main():
    print("Seek Plugin Integrity Check")
    print("===========================")

    # Plugin metadata
    plugin_json = PLUGIN_ROOT / ".claude-plugin" / "plugin.json"
    check(plugin_json.exists(), "plugin.json exists")
    if plugin_json.exists():
        with open(plugin_json) as f:
            p = json.load(f)
        check(p.get("name") == "seek", "Plugin name is 'seek'")

    marketplace_json = PLUGIN_ROOT / ".claude-plugin" / "marketplace.json"
    check(marketplace_json.exists(), "marketplace.json exists")
    if marketplace_json.exists():
        with open(marketplace_json) as f:
            m = json.load(f)
        check(m.get("owner") is not None, "marketplace has owner")
        check(len(m.get("plugins", [])) > 0, "marketplace has plugins array")

    # Skills
    skills_dir = PLUGIN_ROOT / "skills"
    expected = ["orchestrate", "define_context", "review_literature",
                "discover_ideas", "design_ideas", "investigate",
                "communicate", "audit", "crystallize"]
    for s in expected:
        check((skills_dir / s / "SKILL.md").exists(), f"Skill {s}: SKILL.md")
        check((skills_dir / s / "SCHEMA.md").exists(), f"Skill {s}: SCHEMA.md")

    # Standards
    std_dir = PLUGIN_ROOT / "references" / "standards"
    expected_std = ["context-standards", "literature-standards", "idea-standards",
                    "coding-standards", "experiment-standards", "writing-standards",
                    "audit-standards"]
    for s in expected_std:
        check((std_dir / f"{s}.md").exists(), f"Standard: {s}.md")

    # Templates
    templates_dir = PLUGIN_ROOT / "references" / "templates"
    check((templates_dir / "project.state.yaml").exists(), "project.state.yaml")
    check((templates_dir / "code-review-checklist.md").exists(), "code-review-checklist.md")
    check((templates_dir / "claims-audit-checklist.md").exists(), "claims-audit-checklist.md")

    # Configs
    check((PLUGIN_ROOT / "references" / "gate-configs.yml").exists(), "gate-configs.yml")
    check((PLUGIN_ROOT / "references" / "paths.yml").exists(), "paths.yml")
    check((PLUGIN_ROOT / "CLAUDE.md").exists(), "CLAUDE.md")

    # Scripts
    check((PLUGIN_ROOT / "scripts" / "detect_hardware.py").exists(), "detect_hardware.py")
    check((PLUGIN_ROOT / "scripts" / "queue_runner.py").exists(), "queue_runner.py")
    check((PLUGIN_ROOT / "scripts" / "sync_plugin.ps1").exists(), "sync_plugin.ps1")

    print(f"\n{'ALL PASSED' if not ERRORS else f'{len(ERRORS)} FAILURES'}")
    if ERRORS:
        for e in ERRORS:
            print(f"  - {e}")
    return 1 if ERRORS else 0

if __name__ == "__main__":
    sys.exit(main())
