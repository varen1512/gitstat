from src.github_client import GitHubClient
import pandas as pd
from fastapi import FastAPI, HTTPException
app=FastAPI()
import requests

def build_stats(username=None):
        client = GitHubClient(username)
        repos = client.get_repos()
        all_data=[]
        for repo in repos:
            if repo["fork"]:
                  continue
            repo_name = repo["name"]
            commit_stats = client.get_commit_stats(repo_name)
            commit_stats=client.get_commit_stats(repo_name)
            # commits=client.get_commits(repo_name)
            # languages=client.get_languages(repo_name)
            repo_data = {
            "name": repo_name,
            "stars": repo["stargazers_count"],
            "forks": repo["forks_count"],
            "language": repo["language"],
            "url": repo["html_url"],
            "repo_commits_52w": commit_stats["repo_commits"],
            "owner_commits_52w": commit_stats["author_commits"]
            # "commit_count": len(commits),
            # "languages":languages
            }
            all_data.append(repo_data)


        df=pd.DataFrame(all_data)
        return df
@app.get("/")
def root():
    return {"message": "GitStat API is running"}
@app.get("/stats")
def get_stats():
    df = build_stats()

    return {
        "total_repositories": len(df),
        #"total_commits": int(df["commit_count"].sum()),
        "total_stars": int(df["stars"].sum()),
        "total_forks": int(df["forks"].sum()),
        "repo_commits_last_52_weeks": int(df["repo_commits_52w"].sum()),
        "owner_commits_last_52_weeks": int(df["owner_commits_52w"].sum())
        # "average_commits_per_repository": float(
        #     df["commit_count"].mean()
        # )
    }
@app.get("/stats/{username}")
def get_user_stats(username:str):
    try:
        df = build_stats(username)

    except requests.exceptions.HTTPError as error:
        if error.response.status_code == 404:
            raise HTTPException(
                status_code=404,
                detail="GitHub user not found"
            )
        raise HTTPException(
            status_code=502,
            detail="Error communicating with GitHub"
        )
    if df.empty:
            return {
                "username": username,
                "total_repositories": 0,
                "total_stars": 0,
                "total_forks": 0,
                "top_language": None,
                "language_distribution": {},
                "most_starred_repository": None,
                "most_forked_repository": None
        }
    language_counts = df["language"].dropna().value_counts()
    language_distribution = language_counts.to_dict()
    top_language = (
        language_counts.index[0]
        if not language_counts.empty
        else None
)
    most_starred = df.loc[df["stars"].idxmax()]
    most_forked = df.loc[df["forks"].idxmax()]
    return {
        "username": username,
        "total_repositories": len(df),
        "total_stars": int(df["stars"].sum()),
        "total_forks": int(df["forks"].sum()),
        "repo_commits_last_52_weeks": int(df["repo_commits_52w"].sum()),
        "owner_commits_last_52_weeks": int(df["owner_commits_52w"].sum()),
        "language_distribution": language_distribution,
        "top_language": top_language,
        "most_starred_repository": most_starred.to_dict(),
        "most_forked_repository": most_forked.to_dict()
        
        # "total_commits": int(df["commit_count"].sum()),
        # "average_commits_per_repository": float(
        #     df["commit_count"].mean()
        # )
    }









# df.to_csv("data/github_stats.csv", index=False)
# print(df)
# print("\n===== GITHUB ANALYTICS =====")

# print(f"Total repositories: {len(df)}")

# print(f"Total commits: {df['commit_count'].sum()}")

# print(f"Average commits per repository: {df['commit_count'].mean():.2f}")

# most_active = df.loc[df["commit_count"].idxmax()]

# print(f"Most active repository: {most_active['name']}")

# print("\nPrimary languages:")
# print(df["language"].value_counts())