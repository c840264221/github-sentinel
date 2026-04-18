from app.domain.models import RepoData

def summarize(repo_data: RepoData) -> str:
    commits_count = len(repo_data.commits)
    issues_count = len(repo_data.issues)


    return f"""

            Repo: {repo_data.name}
            
            Recent Activity:
            
            * Commits: {commits_count}
            * Issues: {issues_count}
            
            Summary:
            Project is active with ongoing updates.
    """
