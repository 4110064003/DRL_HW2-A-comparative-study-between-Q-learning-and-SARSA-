param(
    [string]$RepoUrl = "https://github.com/4110064003/DRL_HW2-A-comparative-study-between-Q-learning-and-SARSA-.git",
    [string]$TargetDir = (Get-Location).Path,
    [string]$Branch = "main"
)

$ErrorActionPreference = "Stop"

if (Test-Path (Join-Path $TargetDir ".git")) {
    Write-Host "[startup] Existing repo found. Pulling latest from origin/$Branch ..."
    git -C $TargetDir fetch origin $Branch
    git -C $TargetDir checkout $Branch
    git -C $TargetDir pull --ff-only origin $Branch
    Write-Host "[startup] Pull complete."
    exit 0
}

$items = Get-ChildItem -Path $TargetDir -Force
if ($items.Count -eq 0) {
    Write-Host "[startup] Empty directory. Cloning repository into $TargetDir ..."
    git clone --branch $Branch $RepoUrl $TargetDir
    Write-Host "[startup] Clone complete."
    exit 0
}

$repoName = [System.IO.Path]::GetFileNameWithoutExtension($RepoUrl)
$cloneDir = Join-Path $TargetDir $repoName
Write-Host "[startup] Target directory is not empty and not a repo."
Write-Host "[startup] Cloning into subdirectory: $cloneDir"

git clone --branch $Branch $RepoUrl $cloneDir
Write-Host "[startup] Clone complete."
