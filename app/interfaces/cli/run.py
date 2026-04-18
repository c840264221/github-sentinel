from app.core.config import Settings
from app.services.summarizer import fetch_repo_updates
from app.storage.repository import SubscriptionRepository
from app.data.github_client import GitHubClient
from app.services.report_generator import generate_markdown_report
from datetime import datetime, timedelta

settings = Settings()
def run():

    repo = SubscriptionRepository()

    print(repo.get_all())
    since = datetime.now() - timedelta(days=1)
    for repo in settings.default_repos:

        commits = GitHubClient(settings.github_token).fetch_commits(repo)
        issues = GitHubClient(settings.github_token).fetch_issues(repo, since=since)
        pull_requests = GitHubClient(settings.github_token).fetch_pull_requests(repo,since=since)
        summary = fetch_repo_updates(repo, issues, pull_requests, commits=None)
        # print("=" * 40)
        # print(summary)
        generate_markdown_report(repo, issues, pull_requests)
