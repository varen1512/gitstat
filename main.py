from src.github_client import GitHubClient


client = GitHubClient()

repos = client.get_repos()

for repo in repos:
    print(repo["name"])

repos = client.get_repos()

for repo in repos:

    repo_name = repo["name"]

    commits = client.get_commits(repo_name)

    print(repo_name, len(commits))
for commit in commits:
    date = commit["commit"]["author"]["date"]
    print(date)
for repo in repos:
    repo_name=repo["name"]
    language=client.get_languages(repo_name)
    print(language)