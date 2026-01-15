# GitHub Setup Guide

This guide explains how to set up GitHub Pages, GitHub Actions, Environments, and Docker Hub integration for this project.

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [GitHub Pages Setup](#github-pages-setup)
3. [GitHub Environments Setup](#github-environments-setup)
4. [Docker Hub Integration](#docker-hub-integration)
5. [GitHub Actions Secrets](#github-actions-secrets)
6. [Creating the Production Branch](#creating-the-production-branch)
7. [Troubleshooting](#troubleshooting)

---

## Prerequisites

Before starting, ensure you have:

- A GitHub account with repository access
- A Docker Hub account
- Git installed locally
- The repository cloned to your local machine

---

## GitHub Pages Setup

### Step 1: Enable GitHub Pages

1. Go to your repository on GitHub
2. Click **Settings** (gear icon)
3. In the left sidebar, click **Pages**
4. Under **Build and deployment**:
   - **Source**: Select **GitHub Actions**
5. Click **Save**

### Step 2: Verify the docs folder

Ensure your repository has a `docs/` folder containing:
- `index.html` - Your static website
- `.nojekyll` - Prevents Jekyll processing

### Step 3: Trigger deployment

Push changes to the `main` branch to trigger the GitHub Pages deployment:

```bash
git add .
git commit -m "Trigger GitHub Pages deployment"
git push origin main
```

### Step 4: Access your site

After the workflow completes, your site will be available at:
```
https://<username>.github.io/<repository-name>/
```

---

## GitHub Environments Setup

The project uses two environments: **Development** and **Production**.

### Step 1: Create Development Environment

1. Go to **Settings** > **Environments**
2. Click **New environment**
3. Name: `Development`
4. Click **Configure environment**
5. (Optional) Add deployment branch rules:
   - Click **Add deployment branch rule**
   - Select **Selected branches**
   - Add pattern: `main`
6. Click **Save protection rules**

### Step 2: Create Production Environment

1. Go to **Settings** > **Environments**
2. Click **New environment**
3. Name: `Production`
4. Click **Configure environment**
5. **Enable Required reviewers**:
   - Check **Required reviewers**
   - Add yourself or team members as reviewers
   - This enforces manual approval before production deployments
6. Add deployment branch rules:
   - Click **Add deployment branch rule**
   - Select **Selected branches**
   - Add pattern: `production`
7. Click **Save protection rules**

### Environment Configuration Summary

| Environment | Branch | Manual Approval | Docker Tag |
|-------------|--------|-----------------|------------|
| Development | main | No | `dev` |
| Production | production | Yes | `prod` |

---

## Docker Hub Integration

### Step 1: Create Docker Hub Account

1. Go to [hub.docker.com](https://hub.docker.com)
2. Sign up or log in

### Step 2: Create Access Token

1. Click your profile icon > **Account Settings**
2. Go to **Security** > **Access Tokens**
3. Click **New Access Token**
4. Name: `github-actions`
5. Access permissions: **Read, Write, Delete**
6. Click **Generate**
7. **Copy the token** (you won't see it again!)

### Step 3: Create Repository (Optional)

The pipeline will automatically create the repository on first push, but you can create it manually:

1. Click **Create Repository**
2. Name: `todo-app`
3. Visibility: Public or Private
4. Click **Create**

---

## GitHub Actions Secrets

Configure the following secrets in your GitHub repository:

### Step 1: Navigate to Secrets

1. Go to **Settings** > **Secrets and variables** > **Actions**
2. Click **New repository secret**

### Step 2: Add Required Secrets

Add these secrets:

| Secret Name | Value | Description |
|------------|-------|-------------|
| `DOCKER_USERNAME` | Your Docker Hub username | Used for Docker login |
| `DOCKER_PASSWORD` | Your Docker Hub access token | Token from Step 2 above |
| `RENDER_DEPLOY_HOOK_URL` | (Optional) Render deploy hook URL | For Render deployment |

### Adding a Secret

1. Click **New repository secret**
2. Enter the **Name** (e.g., `DOCKER_USERNAME`)
3. Enter the **Value**
4. Click **Add secret**

---

## Creating the Production Branch

### Step 1: Create the branch locally

```bash
# Ensure you're on main and up to date
git checkout main
git pull origin main

# Create and push production branch
git checkout -b production
git push -u origin production
```

### Step 2: Verify branch protection (Optional)

1. Go to **Settings** > **Branches**
2. Click **Add branch protection rule**
3. Branch name pattern: `production`
4. Enable:
   - Require pull request reviews before merging
   - Require status checks to pass before merging
5. Click **Create**

---

## CI/CD Pipeline Overview

The pipeline (`ci-cd.yml`) contains the following jobs:

### 1. Build (`build`)
- Runs on all pushes and pull requests
- Installs dependencies
- Runs linting with flake8
- Creates build artifacts

### 2. Deploy to GitHub Pages (`deploy-pages`)
- Runs after successful build
- Only on `main` branch push
- Deploys `docs/` folder to GitHub Pages

### 3. Deploy to Development (`deploy-development`)
- Runs after successful build
- Only on `main` branch push
- Builds and pushes Docker image with `dev` tag
- Uses Development environment

### 4. Deploy to Production (`deploy-production`)
- Runs after successful build
- Only on `production` branch push
- Requires manual approval (configured in environment)
- Builds and pushes Docker image with `prod` and `latest` tags
- Uses Production environment

### 5. Deploy to Render (`deploy-render`) - Optional
- Runs after Development deployment
- Triggers Render deployment via webhook

---

## Workflow Diagram

```
Push to main branch:
  build --> deploy-pages
        --> deploy-development --> deploy-render (optional)

Push to production branch:
  build --> deploy-production (requires manual approval)
```

---

## Troubleshooting

### GitHub Pages not deploying

1. Check that GitHub Pages source is set to **GitHub Actions**
2. Verify `docs/index.html` exists
3. Check the Actions tab for workflow errors
4. Ensure the workflow has `pages: write` permission

### Docker push failing

1. Verify `DOCKER_USERNAME` and `DOCKER_PASSWORD` secrets are set
2. Ensure the Docker Hub access token has write permissions
3. Check if the repository name is correct

### Production deployment not triggering

1. Ensure you're pushing to the `production` branch
2. Check that the Production environment exists
3. Verify the required reviewers are configured

### Manual approval not appearing

1. Go to **Settings** > **Environments** > **Production**
2. Ensure **Required reviewers** is checked
3. Add at least one reviewer

### Workflow permissions error

If you see permission errors, go to:
1. **Settings** > **Actions** > **General**
2. Under **Workflow permissions**, select **Read and write permissions**
3. Check **Allow GitHub Actions to create and approve pull requests**

---

## Quick Reference

### Triggering Deployments

```bash
# Deploy to Development (and GitHub Pages)
git checkout main
git add .
git commit -m "Your changes"
git push origin main

# Deploy to Production
git checkout production
git merge main
git push origin production
# Then approve the deployment in GitHub Actions
```

### Checking Deployment Status

1. Go to the **Actions** tab
2. Click on the latest workflow run
3. View the status of each job

### Viewing Deployed Images

Visit Docker Hub:
```
https://hub.docker.com/r/<your-username>/todo-app/tags
```

---

## Related Documentation

- [Test Guide](./TEST_GUIDE.md) - How to test the setup
- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [GitHub Pages Documentation](https://docs.github.com/en/pages)
- [Docker Hub Documentation](https://docs.docker.com/docker-hub/)
