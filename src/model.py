from pydantic import BaseModel
from typing import Optional, Dict, Any


class UserStats(BaseModel):
    username: str
    total_repositories: int
    total_stars: int
    total_forks: int

    repo_commits_last_52_weeks: int
    owner_commits_last_52_weeks: int

    language_distribution: Dict[str, int]
    top_language: Optional[str]

    most_starred_repository: Optional[Dict[str, Any]]
    most_forked_repository: Optional[Dict[str, Any]]