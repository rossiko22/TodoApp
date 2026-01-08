# Todo App - CI/CD with GitHub Actions and Render

A simple todo application with Flask backend and vanilla HTML/JS/CSS frontend, featuring a complete CI/CD pipeline with GitHub Actions and deployment to Render.

## Features

- **Backend**: Flask REST API with PostgreSQL database
- **Frontend**: Clean, responsive UI with vanilla JavaScript
- **CI/CD Pipeline**: GitHub Actions with build, Docker, and deploy phases
- **Deployment**: Automated deployment to Render
- **Database**: PostgreSQL on Render, SQLite for local development

## Project Structure

```
.
├── .github/
│   └── workflows/
│       └── ci-cd.yml          # GitHub Actions CI/CD pipeline
├── frontend/
│   ├── index.html             # Frontend HTML
│   ├── style.css              # Frontend CSS
│   └── app.js                 # Frontend JavaScript
├── app.py                     # Flask backend application
├── requirements.txt           # Python dependencies
├── Dockerfile                 # Docker configuration
├── .dockerignore             # Docker ignore file
└── README.md                  # This file
```

## CI/CD Pipeline

The GitHub Actions workflow includes all required phases:

### 1. Build Phase (with Caching)
- Sets up Python 3.11
- Caches pip dependencies using `actions/cache`
- Installs dependencies from `requirements.txt`
- Runs linting with flake8
- Creates build artifacts

### 2. Artifact Storage
- Uploads build artifacts using `actions/upload-artifact`
- Includes frontend files, backend code, and build info
- Artifacts retained for 7 days

### 3. Docker Build Phase
- Uses Docker Buildx for building
- Implements layer caching for faster builds
- Tags images appropriately (latest, branch, SHA)

### 4. Docker Push Phase
- Logs in to Docker Hub using secrets
- Pushes Docker image with multiple tags
- Uses registry cache for optimization

### 5. Deployment Phase
- Triggers Render deployment via API
- Only deploys on push to main/master branch
- Provides deployment summary

## Local Development

### Prerequisites

- Python 3.11+
- pip

### Setup

1. Clone the repository:
```bash
git clone <your-repo-url>
cd rirs-proekt-deploy
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run the application:
```bash
python app.py
```

5. Open your browser and navigate to:
```
http://localhost:5000
```

## Docker Deployment

### Build Docker Image

```bash
docker build -t todo-app .
```

### Run Docker Container

```bash
docker run -p 5000:5000 -e DATABASE_URL=<your-postgres-url> todo-app
```

## Render Deployment

### Step 1: Create PostgreSQL Database on Render

1. Go to [Render Dashboard](https://dashboard.render.com/)
2. Click "New +" and select "PostgreSQL"
3. Fill in the details:
   - Name: `todo-db` (or any name)
   - Database: `todos`
   - User: `todos_user`
   - Region: Choose closest to you
   - Plan: Free
4. Click "Create Database"
5. Copy the "Internal Database URL" (starts with `postgresql://`)

### Step 2: Create Web Service on Render

1. Click "New +" and select "Web Service"
2. Connect your GitHub repository
3. Fill in the details:
   - Name: `todo-app` (or any name)
   - Environment: `Docker`
   - Region: Same as database
   - Branch: `main` (or `master`)
   - Plan: Free

4. Add Environment Variable:
   - Key: `DATABASE_URL`
   - Value: The Internal Database URL from Step 1

5. Click "Create Web Service"

### Step 3: Get Render API Credentials

1. Go to [Render Account Settings](https://dashboard.render.com/account/api-keys)
2. Click "Generate New Key"
3. Copy the API Key
4. Go to your Render service page
5. Copy the Service ID from the URL (e.g., `srv-xxxxxxxxxxxxx`)

### Step 4: Configure GitHub Secrets

Add the following secrets to your GitHub repository:

1. Go to your repository on GitHub
2. Click "Settings" → "Secrets and variables" → "Actions"
3. Click "New repository secret" and add:

   - **DOCKER_USERNAME**: Your Docker Hub username
   - **DOCKER_PASSWORD**: Your Docker Hub password or access token
   - **RENDER_API_KEY**: Your Render API key from Step 3
   - **RENDER_SERVICE_ID**: Your Render service ID from Step 3

### Step 5: Deploy

Push to the main/master branch, and GitHub Actions will:

1. Build the application
2. Create and cache artifacts
3. Build Docker image
4. Push to Docker Hub
5. Deploy to Render

## Docker Hub Setup

1. Create account at [Docker Hub](https://hub.docker.com/)
2. Create a repository named `todo-app`
3. Generate an access token:
   - Account Settings → Security → New Access Token
   - Copy the token and use it as `DOCKER_PASSWORD` secret

## API Endpoints

- `GET /api/health` - Health check
- `GET /api/todos` - Get all todos
- `POST /api/todos` - Create a new todo
  - Body: `{ "title": "Task description" }`
- `PUT /api/todos/:id` - Update a todo
  - Body: `{ "completed": true }` or `{ "title": "New title" }`
- `DELETE /api/todos/:id` - Delete a todo

## Requirements Met

This project satisfies all the assignment requirements:

- ✅ **Build Phase**: Python dependencies installation with pip caching
- ✅ **Caching**: Implements `actions/cache` for pip dependencies
- ✅ **Build Artifacts**: Frontend and backend files stored using `upload-artifact`
- ✅ **Docker Build**: Dockerfile with optimized multi-stage build
- ✅ **Docker Push**: Automated push to Docker Hub with tags
- ✅ **Deployment**: Automated deployment to Render via API
- ✅ **Database**: PostgreSQL integration with connection handling
- ✅ **Frontend-Backend Connection**: REST API integration

## Technologies Used

- **Backend**: Flask, Flask-CORS, psycopg2-binary, gunicorn
- **Frontend**: HTML5, CSS3, Vanilla JavaScript
- **Database**: PostgreSQL (production), SQLite (development)
- **CI/CD**: GitHub Actions
- **Containerization**: Docker
- **Deployment**: Render

## Troubleshooting

### GitHub Actions Fails

- Check that all secrets are properly set in GitHub repository settings
- Verify Docker Hub credentials
- Check Render API key and service ID

### Database Connection Issues

- Verify `DATABASE_URL` environment variable is set on Render
- Check PostgreSQL database is running on Render
- Ensure Internal Database URL is used (not External)

### Docker Build Fails

- Check Dockerfile syntax
- Ensure all files are properly copied
- Verify requirements.txt has all dependencies

### Deployment Issues

- Check Render logs in the dashboard
- Verify environment variables are set
- Ensure the service is not sleeping (Free tier sleeps after inactivity)

## License

MIT License - feel free to use this project for your assignments!
# TodoApp
# TodoApp
# TodoApp
# TodoApp
