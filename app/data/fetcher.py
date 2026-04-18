from app.data.github_client import fetch_commits, fetch_issues
from app.domain.models import RepoData

def fetch_repo(repo: str) -> RepoData:
    commits = fetch_commits(repo)
    issues = fetch_issues(repo)
    return RepoData(name=repo,commits=commits,issues=issues,)


