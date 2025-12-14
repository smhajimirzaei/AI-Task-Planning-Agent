# GitHub Repository Setup Guide

This guide will help you push this project to GitHub.

## Prerequisites

- Git installed on your system
- GitHub account
- Git configured with your credentials

## Step 1: Initialize Git Repository

If not already initialized:

```bash
cd AI_Agent
git init
```

## Step 2: Create .gitignore (Already Done)

The `.gitignore` file is already configured to exclude:
- `.env` files (API keys)
- `credentials.json` and `token.json` (OAuth tokens)
- `*.db` files (database)
- `__pycache__/` and `.pyc` files
- Virtual environment folders

## Step 3: Stage All Files

```bash
git add .
```

## Step 4: Create Initial Commit

```bash
git commit -m "Initial commit: AI Task Planning Agent v1.0.0

- AI-powered task planning with Claude
- Google Calendar and Outlook integration
- Adaptive learning system
- Real-time monitoring and dynamic replanning
- Comprehensive CLI and Python API
- Full documentation and examples"
```

## Step 5: Create GitHub Repository

1. Go to [GitHub](https://github.com)
2. Click the "+" icon → "New repository"
3. Repository name: `AI-Task-Planning-Agent` (or your choice)
4. Description: "An intelligent AI-powered personal task planning and scheduling assistant that learns your habits and preferences over time."
5. Choose Public or Private
6. **DO NOT** initialize with README (we already have one)
7. Click "Create repository"

## Step 6: Add Remote and Push

Replace `YOUR_USERNAME` with your GitHub username:

```bash
# Add remote
git remote add origin https://github.com/YOUR_USERNAME/AI-Task-Planning-Agent.git

# Rename branch to main (if needed)
git branch -M main

# Push to GitHub
git push -u origin main
```

## Step 7: Configure Repository Settings

On GitHub, go to repository Settings:

### General
- Add topics/tags: `ai`, `planning`, `scheduling`, `claude`, `productivity`, `task-management`, `calendar`, `machine-learning`
- Add website (if you have one)

### Issues
- Enable issue templates (already configured in `.github/ISSUE_TEMPLATE/`)

### Security
- Enable vulnerability alerts
- Enable Dependabot alerts

### Actions
- GitHub Actions are configured in `.github/workflows/python-app.yml`
- They will run automatically on push and pull requests

## Step 8: Add Repository Description

Edit your repository and add:

**Description:**
```
An intelligent AI-powered personal task planning and scheduling assistant that learns your habits and preferences over time. Built with Claude AI.
```

**Tags:**
```
ai
task-management
planning
scheduling
claude
productivity
calendar
machine-learning
python
anthropic
google-calendar
adaptive-learning
```

## Step 9: Protect Main Branch (Optional)

For collaboration:

1. Go to Settings → Branches
2. Add branch protection rule for `main`
3. Enable:
   - Require pull request reviews
   - Require status checks to pass
   - Require branches to be up to date

## Step 10: Create Releases (Optional)

1. Go to Releases → Draft a new release
2. Tag version: `v1.0.0`
3. Release title: `v1.0.0 - Initial Release`
4. Copy content from `CHANGELOG.md`
5. Publish release

## Additional Steps

### Create a Wiki (Optional)

Add extended documentation:
- Architecture deep dive
- API reference
- Troubleshooting guide
- FAQ

### Enable Discussions (Optional)

For community engagement:
- Settings → General → Features → Discussions

### Add Funding (Optional)

If you want to accept sponsorships:
- Create `.github/FUNDING.yml`

### Create a Project Board (Optional)

For tracking features and bugs:
- Projects → New project
- Use GitHub's project templates

## Ongoing Maintenance

### Regular Updates

```bash
# After making changes
git add .
git commit -m "Description of changes"
git push
```

### Version Bumping

Update version in:
- `setup.py`
- `CHANGELOG.md`
- Create new release tag

### Keep Dependencies Updated

```bash
pip list --outdated
# Update requirements.txt as needed
```

## Promoting Your Repository

1. **Share on social media** with relevant hashtags
2. **Add to awesome lists** (e.g., awesome-python, awesome-ai-tools)
3. **Write a blog post** about the project
4. **Submit to Product Hunt** or similar platforms
5. **Create demo videos** or GIFs
6. **Engage with the community** in relevant forums

## Repository URLs

After setup, your repository will be at:
- **Repository**: `https://github.com/YOUR_USERNAME/AI-Task-Planning-Agent`
- **Issues**: `https://github.com/YOUR_USERNAME/AI-Task-Planning-Agent/issues`
- **Discussions**: `https://github.com/YOUR_USERNAME/AI-Task-Planning-Agent/discussions`

## Troubleshooting

### Authentication Issues

If you have 2FA enabled, use a Personal Access Token:
1. GitHub → Settings → Developer settings → Personal access tokens
2. Generate new token with `repo` scope
3. Use token as password when pushing

### Large Files

If you accidentally committed large files:
```bash
git rm --cached large_file.db
git commit -m "Remove large file"
git push
```

---

**You're all set!** 🚀

Your AI Task Planning Agent is now ready to share with the world!
