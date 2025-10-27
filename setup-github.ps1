# DevSync Repository Setup Helper
# This script helps you set up the GitHub remote and push your repository

Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "DevSync Repository Setup Helper" -ForegroundColor Cyan
Write-Host "========================================`n" -ForegroundColor Cyan

# Check if we're in a git repository
if (-not (Test-Path ".git")) {
    Write-Host "Error: Not in a git repository!" -ForegroundColor Red
    Write-Host "Please run this script from the q-unicode-data directory" -ForegroundColor Yellow
    exit 1
}

Write-Host "Step 1: Repository Information" -ForegroundColor Green
Write-Host "-------------------------------`n"

# Get GitHub username
$username = Read-Host "Enter your GitHub username"

# Get repository name
Write-Host "`nSuggested repository name: devsync-automated-commits" -ForegroundColor Yellow
$repoName = Read-Host "Enter repository name (or press Enter to use default)"
if ([string]::IsNullOrWhiteSpace($repoName)) {
    $repoName = "devsync-automated-commits"
}

$repoUrl = "https://github.com/$username/$repoName.git"

Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "Repository URL: $repoUrl" -ForegroundColor White
Write-Host "========================================`n" -ForegroundColor Cyan

Write-Host "IMPORTANT: Before continuing, make sure you have:" -ForegroundColor Yellow
Write-Host "1. Created the repository '$repoName' on GitHub" -ForegroundColor Yellow
Write-Host "2. URL: https://github.com/$username/$repoName" -ForegroundColor Yellow
Write-Host "3. DO NOT initialize it with README, .gitignore, or license`n" -ForegroundColor Yellow

$confirm = Read-Host "Have you created the repository on GitHub? (yes/no)"

if ($confirm -ne "yes" -and $confirm -ne "y") {
    Write-Host "`nPlease create the repository first at: https://github.com/new" -ForegroundColor Red
    Write-Host "Then run this script again." -ForegroundColor Yellow
    exit 1
}

Write-Host "`nStep 2: Configuring Git Remote" -ForegroundColor Green
Write-Host "--------------------------------`n"

# Check if remote already exists
$remoteExists = git remote | Select-String -Pattern "origin"

if ($remoteExists) {
    Write-Host "Remote 'origin' already exists. Updating..." -ForegroundColor Yellow
    git remote set-url origin $repoUrl
} else {
    Write-Host "Adding remote 'origin'..." -ForegroundColor Cyan
    git remote add origin $repoUrl
}

# Verify remote
Write-Host "`nVerifying remote..." -ForegroundColor Cyan
git remote -v

Write-Host "`nStep 3: Pushing to GitHub" -ForegroundColor Green
Write-Host "---------------------------`n"

# Rename branch to main if it's master
$currentBranch = git branch --show-current
if ($currentBranch -eq "master") {
    Write-Host "Renaming branch to 'main'..." -ForegroundColor Cyan
    git branch -M main
}

Write-Host "Pushing to GitHub..." -ForegroundColor Cyan
try {
    git push -u origin main
    
    Write-Host "`n========================================" -ForegroundColor Green
    Write-Host "SUCCESS! Repository pushed to GitHub" -ForegroundColor Green
    Write-Host "========================================`n" -ForegroundColor Green
    
    Write-Host "Next Steps:" -ForegroundColor Cyan
    Write-Host "1. Visit: https://github.com/$username/$repoName" -ForegroundColor White
    Write-Host "2. Go to 'Actions' tab" -ForegroundColor White
    Write-Host "3. Click 'Daily Automated Commit' workflow" -ForegroundColor White
    Write-Host "4. Click 'Run workflow' button" -ForegroundColor White
    Write-Host "5. Wait for workflow to complete (green checkmark)" -ForegroundColor White
    Write-Host "6. Verify the commit was created`n" -ForegroundColor White
    
    Write-Host "Your repository URL is:" -ForegroundColor Green
    Write-Host "https://github.com/$username/$repoName`n" -ForegroundColor Yellow
    
} catch {
    Write-Host "`nError pushing to GitHub!" -ForegroundColor Red
    Write-Host "Please check:" -ForegroundColor Yellow
    Write-Host "1. Repository exists on GitHub" -ForegroundColor Yellow
    Write-Host "2. You have proper permissions" -ForegroundColor Yellow
    Write-Host "3. You're logged in to GitHub (may need authentication)`n" -ForegroundColor Yellow
    
    Write-Host "You can try pushing manually with:" -ForegroundColor Cyan
    Write-Host "git push -u origin main`n" -ForegroundColor White
}
