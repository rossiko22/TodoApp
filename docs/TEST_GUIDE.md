# Test Guide

This guide explains how to test and verify that the GitHub Pages, Environments, and CI/CD pipeline are working correctly.

## Table of Contents

1. [Testing Checklist](#testing-checklist)
2. [Testing GitHub Pages](#testing-github-pages)
3. [Testing Development Environment](#testing-development-environment)
4. [Testing Production Environment](#testing-production-environment)
5. [Testing Docker Images](#testing-docker-images)
6. [Verifying Manual Approval](#verifying-manual-approval)
7. [Common Test Scenarios](#common-test-scenarios)

---

## Testing Checklist

Use this checklist to verify all components are working:

### GitHub Pages (30%)
- [ ] `docs/index.html` exists and contains required content
- [ ] `.nojekyll` file exists in docs folder
- [ ] GitHub Pages is enabled with GitHub Actions source
- [ ] Static page is accessible at `https://<user>.github.io/<repo>/`
- [ ] Page displays project name, team members, and description

### Environments (70%)
- [ ] Development environment is created
- [ ] Production environment is created
- [ ] Production environment has required reviewers enabled
- [ ] Docker Hub secrets are configured
- [ ] Docker images are published with correct tags

---

## Testing GitHub Pages

### Test 1: Verify Static Page Content

1. Open `docs/index.html` locally in a browser
2. Verify it contains:
   - Project name: "Todo App"
   - Team member(s): Listed with names
   - Project description: Explanation of the project

### Test 2: Trigger GitHub Pages Deployment

```bash
# Make a small change to trigger deployment
echo "" >> docs/index.html
git add docs/index.html
git commit -m "Test: Trigger GitHub Pages deployment"
git push origin main
```

### Test 3: Verify Deployment

1. Go to **Actions** tab in GitHub
2. Find the latest workflow run
3. Click on it and check the **Deploy to GitHub Pages** job
4. Verify it shows a green checkmark
5. Click the deployment URL in the job summary

### Test 4: Access the Live Site

```
https://<your-username>.github.io/<repository-name>/
```

Expected result: Your static page should be visible with all content.

---

## Testing Development Environment

### Test 1: Verify Environment Exists

1. Go to **Settings** > **Environments**
2. Verify "Development" environment is listed
3. Click on it to see configuration

### Test 2: Trigger Development Deployment

```bash
# Push to main branch
git checkout main
git add .
git commit -m "Test: Development deployment"
git push origin main
```

### Test 3: Verify Workflow Execution

1. Go to **Actions** tab
2. Find the latest workflow run
3. Check that **Deploy to Development** job runs
4. Verify it completes successfully (green checkmark)

### Test 4: Verify Docker Image

1. Go to Docker Hub: `https://hub.docker.com/r/<username>/todo-app/tags`
2. Verify the `dev` tag exists
3. Verify `dev-<commit-sha>` tag exists
4. Check the push timestamp is recent

### Test 5: Pull and Run Docker Image

```bash
# Pull the dev image
docker pull <username>/todo-app:dev

# Run the container
docker run -d -p 5000:5000 --name test-dev <username>/todo-app:dev

# Test the application
curl http://localhost:5000/api/health

# Cleanup
docker stop test-dev
docker rm test-dev
```

---

## Testing Production Environment

### Test 1: Verify Environment Configuration

1. Go to **Settings** > **Environments**
2. Click on "Production"
3. Verify:
   - Required reviewers is enabled
   - At least one reviewer is listed
   - Deployment branch is set to `production`

### Test 2: Create Production Branch (if not exists)

```bash
git checkout main
git checkout -b production
git push -u origin production
```

### Test 3: Trigger Production Deployment

```bash
# Push to production branch
git checkout production
git merge main
git push origin production
```

### Test 4: Verify Manual Approval Required

1. Go to **Actions** tab
2. Find the workflow run for the production push
3. The **Deploy to Production** job should show:
   - Yellow status (waiting)
   - "Waiting for approval" message
4. Click on the job to see approval request

### Test 5: Approve Deployment

1. Click **Review deployments**
2. Check the Production environment
3. Click **Approve and deploy**
4. Enter optional comment
5. Verify deployment continues

### Test 6: Verify Docker Image

1. Go to Docker Hub: `https://hub.docker.com/r/<username>/todo-app/tags`
2. Verify these tags exist:
   - `prod`
   - `prod-<commit-sha>`
   - `latest`

### Test 7: Pull and Run Production Image

```bash
# Pull the prod image
docker pull <username>/todo-app:prod

# Run the container
docker run -d -p 5000:5000 --name test-prod <username>/todo-app:prod

# Test the application
curl http://localhost:5000/api/health

# Cleanup
docker stop test-prod
docker rm test-prod
```

---

## Testing Docker Images

### Verify Image Tags

```bash
# List all available tags
curl -s "https://hub.docker.com/v2/repositories/<username>/todo-app/tags" | jq '.results[].name'
```

Expected tags:
- `dev` - Latest development build
- `dev-<sha>` - Specific development builds
- `prod` - Latest production build
- `prod-<sha>` - Specific production builds
- `latest` - Same as prod

### Compare Image Sizes

```bash
docker images <username>/todo-app
```

### Verify Image Labels

```bash
docker inspect <username>/todo-app:dev --format='{{json .Config.Labels}}' | jq
```

---

## Verifying Manual Approval

### Test: Approval Workflow

1. Push a change to the `production` branch
2. Go to Actions and find the workflow
3. **Verify**: The workflow should pause at the Production deployment
4. Click on the pending job
5. Click **Review deployments**
6. Select the Production environment
7. Click **Approve and deploy**
8. **Verify**: The job continues and completes

### Test: Rejection Workflow

1. Push a change to the `production` branch
2. Go to Actions and find the workflow
3. Click **Review deployments**
4. Select the Production environment
5. Click **Reject**
6. **Verify**: The job is cancelled

---

## Common Test Scenarios

### Scenario 1: Full Development Cycle

```bash
# 1. Make a change
echo "// Test change" >> app.py
git add app.py
git commit -m "Test: Development cycle"
git push origin main

# 2. Wait for pipeline
# Check Actions tab

# 3. Verify results
# - GitHub Pages updated
# - Docker Hub has new dev image
# - Development deployment successful
```

### Scenario 2: Full Production Cycle

```bash
# 1. Merge to production
git checkout production
git merge main
git push origin production

# 2. Wait for pipeline (will pause)
# Check Actions tab

# 3. Approve deployment
# Click Review deployments > Approve

# 4. Verify results
# - Docker Hub has new prod image
# - Production deployment successful
```

### Scenario 3: Verify Branch Restrictions

```bash
# 1. Try pushing directly to production
git checkout production
echo "// Direct change" >> app.py
git commit -am "Direct production push"
git push origin production

# 2. Verify the workflow still requires approval
# (Environment protection rules apply)
```

---

## Automated Test Script

Create and run this script to test the Docker images:

```bash
#!/bin/bash
# test-docker-images.sh

DOCKER_USER="your-docker-username"
IMAGE="$DOCKER_USER/todo-app"

echo "=== Testing Docker Images ==="

# Test dev image
echo "Testing dev image..."
docker pull $IMAGE:dev
docker run -d -p 5001:5000 --name test-dev $IMAGE:dev
sleep 5
DEV_RESULT=$(curl -s http://localhost:5001/api/health)
echo "Dev health check: $DEV_RESULT"
docker stop test-dev && docker rm test-dev

# Test prod image (if exists)
echo "Testing prod image..."
if docker pull $IMAGE:prod 2>/dev/null; then
    docker run -d -p 5002:5000 --name test-prod $IMAGE:prod
    sleep 5
    PROD_RESULT=$(curl -s http://localhost:5002/api/health)
    echo "Prod health check: $PROD_RESULT"
    docker stop test-prod && docker rm test-prod
else
    echo "Prod image not found - deploy to production first"
fi

echo "=== Tests Complete ==="
```

---

## Verification Summary

After testing, you should have verified:

| Component | Test | Expected Result |
|-----------|------|-----------------|
| GitHub Pages | Access live URL | Static page visible |
| index.html | Check content | Project info displayed |
| Development env | Push to main | Deploys automatically |
| Production env | Push to production | Requires approval |
| Docker dev tag | Check Docker Hub | Image with `dev` tag |
| Docker prod tag | Check Docker Hub | Image with `prod` tag |
| Manual approval | Deploy to production | Workflow pauses |

---

## Troubleshooting Tests

### Pages not loading

1. Check if workflow completed successfully
2. Verify GitHub Pages settings
3. Wait a few minutes for DNS propagation

### Docker images not appearing

1. Check Docker Hub credentials
2. Verify workflow logs for push errors
3. Ensure repository exists on Docker Hub

### Manual approval not working

1. Verify Production environment exists
2. Check required reviewers is enabled
3. Ensure you're pushing to `production` branch

---

## Related Documentation

- [GitHub Setup Guide](./GITHUB_SETUP_GUIDE.md) - Initial setup instructions
- [CI/CD Pipeline](./../.github/workflows/ci-cd.yml) - Workflow definition
