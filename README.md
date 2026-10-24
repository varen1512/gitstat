# GitStat — GitHub Repository Analytics

GitStat is a GitHub analytics application that turns repository and contribution data into useful statistics. It uses the GitHub REST API to collect repository information, FastAPI to serve analytics, PostgreSQL to cache results, and React to provide a dashboard.

## Features

- **Repository analytics** — View repository count, stars, and forks.
- **Language insights** — Explore programming language distribution and identify your top language.
- **Repository highlights** — Find your most-starred and most-forked repositories.
- **Commit analytics** — Track repository commits and owner contributions over the last 52 weeks.
- **REST API** — Retrieve analytics for a GitHub user through a FastAPI endpoint.
- **Database caching** — Store computed statistics in PostgreSQL to reduce repeated GitHub API requests.
- **Interactive dashboard** — Visualize analytics through a React frontend.
- **Automated tests** — Validate backend functionality with pytest.
- **Docker support** — Run the backend in a container.

## Tech Stack

| Component | Technology |
|---|---|
| Backend | Python, FastAPI |
| Data processing | Pandas |
| Data source | GitHub REST API |
| Database and caching | PostgreSQL, JSONB |
| Frontend | React, JavaScript |
| Testing | pytest |
| Containerization | Docker |

## Project Structure

```text
gitstat/
├── src/
│   ├── __init__.py
│   ├── database.py
│   ├── github_client.py
│   └── model.py
├── tests/
│   └── test_main.py
├── frontend/
├── data/
├── main.py
├── Dockerfile
├── .dockerignore
├── .gitignore
├── requirements.txt
└── README.md
```

## Getting Started

### Prerequisites

- Python 3.10 or later
- PostgreSQL
- Node.js and npm for the frontend
- A GitHub personal access token

### 1. Clone the repository

```bash
git clone https://github.com/varen1512/gitstat.git
cd gitstat
```

### 2. Set up the Python environment

```bash
python3 -m venv .my_venv
source .my_venv/bin/activate
pip install -r requirements.txt
```

### 3. Configure environment variables

Create a `.env` file in the project root:

```env
GITHUB_TOKEN=your_github_token
DATABASE_URL=postgresql://username:password@localhost:5432/gitstat_db
```

Replace the example values with your own credentials and PostgreSQL connection details. Never commit your `.env` file or expose your GitHub token.

### 4. Set up PostgreSQL

Create a PostgreSQL database named `gitstat_db` and configure the connection string in `.env`.

Ensure the `stats_cache` table exists with the schema expected by `src/database.py` before running the application.

### 5. Run the backend

```bash
uvicorn main:app --reload
```

The API should now be available at:

- API root: `http://127.0.0.1:8000/`
- Interactive API documentation: `http://127.0.0.1:8000/docs`

## API Usage

### Get analytics for a GitHub user

```http
GET /stats/{username}
```

Example:

```http
GET /stats/varen1512
```

The response includes analytics such as:

- Total repositories
- Total stars and forks
- Language distribution and top language
- Most-starred and most-forked repositories
- Repository commits over the last 52 weeks
- Owner contributions over the last 52 weeks

The exact response fields depend on the current API implementation.

## Database Caching

GitStat uses PostgreSQL to store computed statistics for GitHub users. Cached results can reduce repeated API calls and improve response times.

The cache uses a time-to-live (TTL) policy. Once a cached entry expires, the application can refresh the statistics from GitHub and save the updated results.

## Frontend

The React dashboard is located in the `frontend/` directory.

To run it locally:

```bash
cd frontend
npm install
npm run dev
```

Make sure the backend is running and that the frontend is configured to call the correct API URL.

## Run Tests

From the project root, activate your Python environment and run:

```bash
pytest -v
```

## Run with Docker

Build the backend image from the project root:

```bash
docker build -t gitstat-backend .
```

Run the container:

```bash
docker run --rm \
  --name gitstat-api \
  -p 8000:8000 \
  --env-file .env \
  -e DATABASE_URL="postgresql://username:password@host.docker.internal:5432/gitstat_db" \
  gitstat-backend
```

Replace the database username and password with your own. On Docker Desktop for macOS, `host.docker.internal` allows the container to reach a PostgreSQL instance running on the host machine. Ensure PostgreSQL is running and the cache table has been created.

## Future Improvements

- Deploy the API and dashboard publicly.
- Improve cache invalidation and database initialization.
- Add more repository and contribution visualizations.
- Improve error handling and API rate-limit management.
- Add continuous integration and automated deployment.

## Author

**Varen Kumar**

- GitHub: [@varen1512](https://github.com/varen1512)
- LinkedIn: [Varen Kumar](https://www.linkedin.com/in/varen-kumar-09a56422a/)

---

Built to explore GitHub data through practical backend development, data processing, database caching, and frontend visualization.
