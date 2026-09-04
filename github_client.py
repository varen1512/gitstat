import os
import requests
from dotenv import load_dotenv


class GitHubClient:

    def __init__(self):
        load_dotenv()

        self.token = os.getenv("GITHUB_TOKEN")
        self.username = os.getenv("GITHUB_USERNAME")

        self.headers = {
            "Authorization": f"Bearer {self.token}",
            "Accept": "application/vnd.github+json"
        }

    def get_repos(self):
        url = f"https://api.github.com/users/{self.username}/repos"

        response = requests.get(
            url,
            headers=self.headers
        )

        response.raise_for_status()

        return response.json()