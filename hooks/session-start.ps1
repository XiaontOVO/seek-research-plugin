# Seek Plugin — Session Start Hook
# Health check + context injection for the Seek research pipeline.

$pluginRoot = $env:CLAUDE_PLUGIN_ROOT
if (-not $pluginRoot) {
    Write-Warning "Seek: CLAUDE_PLUGIN_ROOT not set — skipping health check."
    exit 0
}

# === Health Check ===
$skillCount = (Get-ChildItem -Path "$pluginRoot/skills" -Directory).Count
$standardsCount = (Get-ChildItem -Path "$pluginRoot/references/standards" -File).Count
$refFiles = @(
    "$pluginRoot/references/paths.yml",
    "$pluginRoot/references/acceptance-criteria-rules.md",
    "$pluginRoot/references/templates/pipeline-state.yml"
)

$healthy = $true
if ($skillCount -ne 8) {
    Write-Warning "Seek: Expected 8 skills, found $skillCount."
    $healthy = $false
}
if ($standardsCount -ne 7) {
    Write-Warning "Seek: Expected 7 standards, found $standardsCount."
    $healthy = $false
}
foreach ($f in $refFiles) {
    if (-not (Test-Path $f)) {
        Write-Warning "Seek: Missing reference file: $f"
        $healthy = $false
    }
}

$status = if ($healthy) { "HEALTHY" } else { "DEGRADED" }

# === Context Injection ===
Write-Output @"
[Seek Plugin — $status]

Seek is a foolproof research pipeline: Project - Phase - Stage - Step
with validation gates and mandatory standards at every level.

Pipeline order:
  define_context → review_literature → design_ideas → investigate → communicate → audit

Standards enforced before every phase:
  coding-standards.md | experiment-standards.md | literature-standards.md
  idea-standards.md | writing-standards.md | audit-standards.md

To start research:
  /seeker        — enter the pipeline (orchestrator tells you what to do next)

Core principle:
  LOAD STANDARDS → EXECUTE → CHECK AGAINST STANDARDS → PASS/FAIL
  No standard, no action. No checklist, no done.

Repair strategy:
  Validation FAIL → re-invoke phase skill with feedback (max 3 repair attempts)

Session-start hook loaded successfully.
"@
