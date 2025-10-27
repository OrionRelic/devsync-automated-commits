# DevSync Repository Setup Instructions

## Step 1: Create GitHub Repository

1. Go to https://github.com/new
2. Repository name: `devsync-automated-commits` (or your preferred name)
3. Description: "DevSync automated daily commit workflow repository"
4. Choose: Public or Private (your preference)
5. **DO NOT** initialize with README, .gitignore, or license (we already have these)
6. Click "Create repository"

## Step 2: Connect Local Repository to GitHub

After creating the repository on GitHub, run these commands:

```powershell
# Add the remote repository (replace YOUR_USERNAME with your GitHub username)
git remote add origin https://github.com/YOUR_USERNAME/devsync-automated-commits.git

# Verify the remote was added
git remote -v

# Push your code to GitHub
git branch -M main
git push -u origin main
```

## Step 3: Verify the Workflow File

After pushing:
1. Go to your repository on GitHub
2. Navigate to `.github/workflows/daily-commit.yml`
3. Verify the file is present and properly formatted

## Step 4: Manually Trigger the Workflow

To test the workflow immediately:

1. Go to your repository on GitHub
2. Click on the "Actions" tab
3. You should see "Daily Automated Commit" workflow
4. Click on the workflow name
5. Click "Run workflow" button (on the right side)
6. Select "Branch: main"
7. Click "Run workflow"

## Step 5: Wait for Workflow Completion

1. The workflow will start running (you'll see a yellow dot)
2. Wait for it to complete (green checkmark means success)
3. This should take about 30-60 seconds

## Step 6: Verify the Commit

After the workflow completes:
1. Go back to the main repository page
2. You should see a new commit with message like "chore: Daily automated update - [timestamp]"
3. Check the commit author - should be "DevSync Automation"
4. Check the commit email - should be "24f1002783@ds.study.iitm.ac.in"

## Step 7: Check the Logs

1. Navigate to the `logs/` directory in your repository
2. You should see:
   - Updated `daily-updates.log`
   - New file `activity-YYYY-MM-DD.txt` with today's date

## Step 8: Submit Your Repository URL

Once verified, your repository URL will be in the format:
```
https://github.com/YOUR_USERNAME/devsync-automated-commits
```

## Workflow Details

The workflow is configured to:
- Run daily at 09:30 UTC (scheduled)
- Can be triggered manually for testing
- Creates commit with your email (24f1002783@ds.study.iitm.ac.in)
- Generates daily activity logs
- Commits changes automatically

## Troubleshooting

If the workflow fails:
1. Check the Actions tab for error messages
2. Ensure the workflow file syntax is correct
3. Verify repository permissions
4. Check that the GITHUB_TOKEN has proper permissions

## Scheduled Runs

After the initial manual trigger:
- The workflow will run automatically every day at 09:30 UTC
- No manual intervention required
- All commits will be tracked in your repository history
