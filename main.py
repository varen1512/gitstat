from src.github_client import GitHubClient
import pandas as pd

client = GitHubClient()

repos = client.get_repos()
all_data=[]
for repo in repos:
    repo_name = repo["name"]
    commits=client.get_commits(repo_name)
    languages=client.get_languages(repo_name)
    repo_data = {
    "name": repo_name,
    "stars": repo["stargazers_count"],
    "forks": repo["forks_count"],
    "language": repo["language"],
    "url": repo["html_url"],
    "commit_count": len(commits),
    "languages":languages
    }
    all_data.append(repo_data)


df=pd.DataFrame(all_data)

df.to_csv("data/github_stats.csv", index=False)
print(df)
print("\n===== GITHUB ANALYTICS =====")

print(f"Total repositories: {len(df)}")

print(f"Total commits: {df['commit_count'].sum()}")

print(f"Average commits per repository: {df['commit_count'].mean():.2f}")

most_active = df.loc[df["commit_count"].idxmax()]

print(f"Most active repository: {most_active['name']}")

print("\nPrimary languages:")
print(df["language"].value_counts())