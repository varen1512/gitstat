from fastapi.testclient import TestClient
from main import app
import pandas as pd
from unittest.mock import patch
client = TestClient(app)


def test_root():
    response = client.get("/")

    assert response.status_code == 200
    assert response.json() == {
        "message": "GitStat API is running"
    }
def test_stats():

    fake_data = pd.DataFrame([
        {
            "name": "repo-one",
            "commit_count": 10
        },
        {
            "name": "repo-two",
            "commit_count": 20
        }
    ])

    with patch("main.build_stats", return_value=fake_data):
        response = client.get("/stats")

    assert response.status_code == 200

    data = response.json()

    assert data["total_repositories"] == 2
    assert data["total_commits"] == 30
    assert data["average_commits_per_repository"] == 15.0