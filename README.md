# GitStat

GitStat is a Python-based GitHub analytics project that collects repository data using the GitHub REST API and exposes basic statistics through a FastAPI backend.

The project currently fetches live repository, commit, and language data from GitHub, processes it using Pandas, and provides summary statistics through an API endpoint.

## Features

- Fetch repositories from the GitHub API
- Fetch commit history with pagination
- Fetch programming language data for repositories
- Process repository data using Pandas
- Calculate basic GitHub statistics
- Expose statistics through a FastAPI REST API
- Automated API tests using Pytest
- Mock external data during testing to avoid unnecessary GitHub API requests

## Tech Stack

- Python
- FastAPI
- Pandas
- Requests
- Pytest
- GitHub REST API
- python-dotenv

## Project Structure

```text
gitstat/
├── src/
│   ├── __init__.py
│   ├── github_client.py
│   └── models.py
├── tests/
│   └── test_main.py
├── data/
├── main.py
├── requirements.txt
├── .gitignore
└── README.md
```

## Setup

### 1. Clone the repository

```bash
git clone https://github.com/varen1512/gitstat.git
cd gitstat
```

### 2. Create a virtual environment

```bash
python3 -m venv .my_venv
```

Activate it on macOS/Linux:

```bash
source .my_venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file in the project root:

```env
GITHUB_TOKEN=your_github_token
GITHUB_USERNAME=your_github_username
```

The `.env` file is ignored by Git and should never be committed to the repository.

## Running the API

Start the FastAPI development server:

```bash
uvicorn main:app --reload
```

If port `8000` is already in use:

```bash
uvicorn main:app --reload --port 8001
```

FastAPI's interactive API documentation is available at:

```text
http://127.0.0.1:8000/docs
```

Use port `8001` instead if the server was started on port 8001.

## API Endpoints

### `GET /`

Checks whether the API is running.

Example response:

```json
{
  "message": "GitStat API is running"
}
```

### `GET /stats`

Fetches live GitHub data and returns basic statistics for the configured GitHub account.

Example response:

```json
{
  "total_repositories": 10,
  "total_commits": 150,
  "average_commits_per_repository": 15.0
}
```

Actual values depend on the GitHub account configured in `.env`.

## Running Tests

Run the test suite using:

```bash
python -m pytest -vv
```

The current tests verify:

- The root API endpoint responds correctly
- The `/stats` endpoint calculates statistics correctly
- GitHub-dependent statistics can be tested using mocked data instead of making live API requests

## Current Status

GitStat currently provides a working FastAPI backend around the GitHub statistics pipeline with automated API tests.

Future development can extend the project with additional analytics, support for arbitrary GitHub usernames, persistent storage, visualization, and deployment.

## Author

**Varen Kumar**

GitHub: `varen1512`