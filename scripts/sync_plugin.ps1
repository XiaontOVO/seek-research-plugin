# Seek Plugin — Sync from GitHub
# Updates the installed plugin to the latest version from the repository.
param(
    [string]$RepoUrl = "https://github.com/XiaontOVO/seek-research-plugin.git",
    [string]$InstallDir = "$env:USERPROFILE\.claude\plugins\marketplaces\seek-research-plugin"
)

Write-Host "Seek Plugin Sync" -ForegroundColor Cyan
Write-Host "================" -ForegroundColor Cyan

if (Test-Path "$InstallDir\.git") {
    Write-Host "Existing installation found. Pulling latest..." -ForegroundColor Green
    Push-Location $InstallDir
    git pull origin master 2>&1 | Write-Host
    Pop-Location
} else {
    Write-Host "No existing installation. Cloning..." -ForegroundColor Yellow
    New-Item -ItemType Directory -Force -Path $InstallDir | Out-Null
    git clone $RepoUrl $InstallDir 2>&1 | Write-Host
}

Write-Host ""
Write-Host "Verifying installation..." -ForegroundColor Cyan

$skillCount = (Get-ChildItem -Path "$InstallDir\skills" -Directory).Count
$standardsCount = (Get-ChildItem -Path "$InstallDir\references\standards" -File).Count

if ($skillCount -eq 9) {
    Write-Host "  Skills: 9/9 OK" -ForegroundColor Green
} else {
    Write-Host "  Skills: $skillCount/9 MISSING" -ForegroundColor Red
}

if ($standardsCount -ge 7) {
    Write-Host "  Standards: $standardsCount OK" -ForegroundColor Green
} else {
    Write-Host "  Standards: $standardsCount (expected >= 7)" -ForegroundColor Red
}

Write-Host ""
Write-Host "Sync complete. Restart Claude Code to reload." -ForegroundColor Green
