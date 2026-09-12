import os
import requests
from dotenv import load_dotenv
import logging
# logging.basicConfig(
#     level=logging.INFO,
#     format="%(asctime)s - %(levelname)s - %(message)s"
# )



logger = logging.getLogger(__name__)


class GitHubClient:

    def __init__(self):
        load_dotenv()

        self.token = os.getenv("GITHUB_TOKEN")
        self.username = os.getenv("GITHUB_USERNAME")
        logger.debug(f"Username: {self.username}")
        logger.debug(f"Token exists: {self.token is not None}")
        self.headers = {
            "Authorization": f"Bearer {self.token}",
            "Accept": "application/vnd.github+json"
        }

    def get_repos(self):
        url = f"https://api.github.com/users/{self.username}/repos"
        logger.info(f"Fetching repos for user: {self.username}")

        response = requests.get(
            url,
            headers=self.headers
        )
        response.raise_for_status()

        repos = response.json()
        logger.info(f"Fetched {len(repos)} repos")
        return repos

    def get_commits(self, repo_name):
        url = (
            f"https://api.github.com/repos/"
            f"{self.username}/{repo_name}/commits"
        )
        
        logger.info(f"Fetching commits for repo: {repo_name}")
        all_commits=[]
        page=1
        while True:
            response = requests.get(
                url,
                headers=self.headers,
                params={
                    "per_page":100,
                    "page":page
                    }
                )
            response.raise_for_status()
            commits = response.json()
            if not commits:
                logger.info(f"No more commits found for {repo_name} on page {page}")
                break
            all_commits.extend(commits)
            page+=1
        logger.info(f"Fetched {len(all_commits)} commits for {repo_name}")
        return all_commits
        

    def get_languages(self, repo_name):
        url = (
            f"https://api.github.com/repos/"
            f"{self.username}/{repo_name}/languages"
        )
        logger.info(f"Fetching languages for repo: {repo_name}")

        response = requests.get(
            url,
            headers=self.headers
        )
        response.raise_for_status()

        return response.json()