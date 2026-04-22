param(
    [string]$RepoUrl = "https://github.com/4110064003/DRL_HW2-A-comparative-study-between-Q-learning-and-SARSA-.git",
    [string]$Branch = "main",
    [string]$CommitMessage = "chore: update HW2 project"
)

$ErrorActionPreference = "Stop"
$RepoDir = (Get-Location).Path

if (-not (Test-Path (Join-Path $RepoDir ".git"))) {
    Write-Host "[ending] No git repo detected. Initializing repository ..."
    git init
    git checkout -B $Branch
}

$originUrl = ""
try {
    $originUrl = (git remote get-url origin) 2>$null
} catch {
    $originUrl = ""
}

if (-not $originUrl) {
    Write-Host "[ending] Adding remote origin ..."
    git remote add origin $RepoUrl
}

Write-Host "[ending] Staging all changes ..."
git add -A

$hasStaged = (git diff --cached --name-only)
if (-not $hasStaged) {
    Write-Host "[ending] No staged changes to commit."
} else {
    Write-Host "[ending] Committing changes ..."
    git commit -m $CommitMessage
}

Write-Host "[ending] Pushing to origin/$Branch ..."
git push -u origin $Branch
Write-Host "[ending] Push complete."
