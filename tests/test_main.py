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
        "stars": 5,
        "forks": 2,
        "language": "Python"
    },
    {
        "name": "repo-two",
        "stars": 10,
        "forks": 3,
        "language": "C++"
    }
])

    with patch("main.build_stats", return_value=fake_data):
        response = client.get("/stats")

    assert response.status_code == 200

    data = response.json()

    assert data["total_repositories"] == 2
    assert data["total_stars"] == 15
    assert data["total_forks"] == 5
def test_user_stats():
    fake_data = pd.DataFrame([
        {
            "name": "repo-one",
            "stars": 5,
            "forks": 2,
            "language": "Python"
        },
        {
            "name": "repo-two",
            "stars": 10,
            "forks": 3,
            "language": "C++"
        }
    ])
    
    with patch("main.build_stats", return_value=fake_data) as mock_build:
        response = client.get("/stats/octocat")

    assert response.status_code == 200

    data = response.json()

    assert data["username"] == "octocat"
    assert data["total_repositories"] == 2
    assert data["total_stars"] == 15
    assert data["total_forks"] == 5

    mock_build.assert_called_once_with("octocat")