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

Write-Host "`nSeek Plugin Sync`n================" -ForegroundColor Cyan

# Step 1: Push from dev to GitHub
Write-Host "`n[1/3] Pushing to GitHub..." -ForegroundColor Yellow
Push-Location $DevDir
$status = git status --porcelain
if ($status) {
    Write-Host "  Uncommitted changes found. Committing..." -ForegroundColor Yellow
    git add -A
    git commit -m "sync: auto-commit from dev" 2>&1 | Out-Null
}
git push origin master 2>&1 | ForEach-Object { Write-Host "  $_" }
Pop-Location
Write-Host "  Push complete." -ForegroundColor Green

# Step 2: Pull from GitHub to marketplaces
Write-Host "`n[2/3] Updating marketplaces..." -ForegroundColor Yellow
if (Test-Path "$MarketplaceDir\.git") {
    Push-Location $MarketplaceDir
    git pull origin master 2>&1 | ForEach-Object { Write-Host "  $_" }
    Pop-Location
} else {
    Write-Host "  No git repo in marketplaces. Cloning fresh..." -ForegroundColor Yellow
    Remove-Item -Recurse -Force $MarketplaceDir -ErrorAction SilentlyContinue
    git clone $RepoUrl $MarketplaceDir 2>&1 | ForEach-Object { Write-Host "  $_" }
}
Write-Host "  Marketplaces updated." -ForegroundColor Green

# Step 3: Copy to cache
Write-Host "`n[3/3] Updating cache..." -ForegroundColor Yellow
Remove-Item -Recurse -Force $CacheDir -ErrorAction SilentlyContinue
New-Item -ItemType Directory -Force -Path $CacheDir | Out-Null
Copy-Item -Recurse -Force "$MarketplaceDir\*" $CacheDir
Write-Host "  Cache updated." -ForegroundColor Green

# Verify
Write-Host "`nVerification:" -ForegroundColor Cyan
$skillCount = (Get-ChildItem -Path "$MarketplaceDir\skills" -Directory -ErrorAction SilentlyContinue).Count
$cacheSkillCount = (Get-ChildItem -Path "$CacheDir\seek\skills" -Directory -ErrorAction SilentlyContinue).Count
Write-Host "  Marketplaces: $skillCount skills" -ForegroundColor $(if ($skillCount -eq 9) { "Green" } else { "Red" })
Write-Host "  Cache: $cacheSkillCount skills" -ForegroundColor $(if ($cacheSkillCount -eq 9) { "Green" } else { "Red" })

Write-Host "`nSync complete. Restart Claude Code to reload.`n" -ForegroundColor Green
