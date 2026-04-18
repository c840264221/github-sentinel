from app.core.config import Settings
from app.services.summarizer import summarize
from app.storage.repository import SubscriptionRepository
from app.data.github_client import GitHubClient
from app.domain.models import RepoData


settings = Settings()
def run():

    repo = SubscriptionRepository()

    print(repo.get_all())

    for repo in settings.default_repos:
        commits = GitHubClient(settings.github_token).fetch_commits(repo)
        issues = GitHubClient(settings.github_token).fetch_issues(repo)
        summary = summarize(RepoData(name=repo, commits=commits, issues=issues, ))
        print("=" * 40)
        print(summary)
