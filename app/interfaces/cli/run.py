from app.core.config import Settings
from app.storage.repository import SubscriptionRepository
from app.data.github_client import GitHubClient
from app.services.report_generator import ReportGenerator
from datetime import datetime, timedelta
from app.services.llm.ollama_client import OllamaClient

settings = Settings()
def run():

    repo = SubscriptionRepository()
    llm = OllamaClient()
    report_generator = ReportGenerator(llm)

    print(repo.get_all())
    since = datetime.now() - timedelta(days=1)
    for repo in settings.default_repos:

        issues = GitHubClient(settings.github_token).fetch_issues(repo, since=since)
        pull_requests = GitHubClient(settings.github_token).fetch_pull_requests(repo,since=since)
        if issues == 'EXIST' and pull_requests == 'EXIST':\
            print('The data was already fetched and the MD-File was spawned!')
        else:
            markdown_path = report_generator.generate_raw_markdown_report(repo, issues, pull_requests)
            report_generator.generate_process_markdown_report(markdown_path)
