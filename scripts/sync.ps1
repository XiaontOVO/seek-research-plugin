# Seek Plugin — Sync Script
# 1. Push latest changes to GitHub
# 2. Pull from GitHub to marketplaces
# 3. Copy to cache for Claude Code
param(
    [string]$DevDir = "D:\Research\plugin\seek",
    [string]$MarketplaceDir = "$env:USERPROFILE\.claude\plugins\marketplaces\seek",
    [string]$CacheDir = "$env:USERPROFILE\.claude\plugins\cache\seek",
    [string]$RepoUrl = "https://github.com/XiaontOVO/seek-research-plugin.git"
)

$ErrorActionPreference = "Stop"

Write-Host "`nSeek Plugin Sync`n================" -ForegroundColor Cyan

# Step 1: Push from dev to GitHub
Write-Host "`n[1/3] Pushing to GitHub..." -ForegroundColor Yellow
Push-Location $DevDir
try {
    $status = git status --porcelain
    if ($status) {
        Write-Host "  Uncommitted changes:" -ForegroundColor Yellow
        git status --short
        Write-Host "  Committing with user-provided message..." -ForegroundColor Yellow
        git add -A
        git commit -m "sync: $(Get-Date -Format 'yyyy-MM-dd HH:mm')" 2>&1 | ForEach-Object { Write-Host "  $_" }
    }
    git push origin master 2>&1 | ForEach-Object { Write-Host "  $_" }
    if ($LASTEXITCODE -ne 0) { throw "git push failed" }
    Write-Host "  Push complete." -ForegroundColor Green
} finally {
    Pop-Location
}

# Step 2: Pull from GitHub to marketplaces
Write-Host "`n[2/3] Updating marketplaces..." -ForegroundColor Yellow
if (Test-Path "$MarketplaceDir\.git") {
    Push-Location $MarketplaceDir
    try {
        git pull origin master 2>&1 | ForEach-Object { Write-Host "  $_" }
        if ($LASTEXITCODE -ne 0) { throw "git pull failed" }
    } finally {
        Pop-Location
    }
} else {
    Write-Host "  No git repo in marketplaces. Cloning fresh..." -ForegroundColor Yellow
    Remove-Item -Recurse -Force $MarketplaceDir -ErrorAction SilentlyContinue
    git clone $RepoUrl $MarketplaceDir 2>&1 | ForEach-Object { Write-Host "  $_" }
    if ($LASTEXITCODE -ne 0) { throw "git clone failed" }
}
Write-Host "  Marketplaces updated." -ForegroundColor Green

# Step 3: Copy to cache (mirror, non-destructive)
Write-Host "`n[3/3] Updating cache..." -ForegroundColor Yellow
New-Item -ItemType Directory -Force -Path "$CacheDir\seek" | Out-Null
robocopy "$MarketplaceDir" "$CacheDir\seek" /E /PURGE /NFL /NDL /NJH /NJS
if ($LASTEXITCODE -ge 8) { throw "robocopy failed with exit code $LASTEXITCODE" }
Write-Host "  Cache mirrored from marketplaces." -ForegroundColor Green

# Verify — count skills dynamically
Write-Host "`nVerification:" -ForegroundColor Cyan
$skillCount = (Get-ChildItem -Path "$MarketplaceDir\skills" -Directory -ErrorAction SilentlyContinue).Count
$cacheSkillCount = (Get-ChildItem -Path "$CacheDir\seek\skills" -Directory -ErrorAction SilentlyContinue).Count
$expectedSkillCount = (Get-ChildItem -Path "$DevDir\skills" -Directory).Count
Write-Host "  Dev: $expectedSkillCount skills" -ForegroundColor White
Write-Host "  Marketplaces: $skillCount skills" -ForegroundColor $(if ($skillCount -eq $expectedSkillCount) { "Green" } else { "Red" })
Write-Host "  Cache: $cacheSkillCount skills" -ForegroundColor $(if ($cacheSkillCount -eq $expectedSkillCount) { "Green" } else { "Red" })

Write-Host "`nSync complete. Restart Claude Code to reload.`n" -ForegroundColor Green
