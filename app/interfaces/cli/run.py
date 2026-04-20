from app.core.config import Settings
from app.storage.repository import SubscriptionRepository
from app.data.github_client import GitHubClient
from app.services.report_generator import ReportGenerator
from datetime import datetime, timedelta
from app.services.llm.ollama_client import OllamaClient
from app.core.logger import get_logger


logger = get_logger(__name__)

settings = Settings()
def run():

    repo = SubscriptionRepository()
    llm = OllamaClient()
    report_generator = ReportGenerator(llm)

    since = datetime.now() - timedelta(days=1)
    for repo in settings.default_repos:
        logger.info(f"Fetching repo {repo}")
        issues = GitHubClient(settings.github_token).fetch_issues(repo, since=since)
        pull_requests = GitHubClient(settings.github_token).fetch_pull_requests(repo,since=since)
        if issues == 'EXIST' and pull_requests == 'EXIST':
            logger.info(f"⏭ Skip {repo}, already fetched. since {since}")
            print('The data was already fetched and the MD-File was spawned!')
        else:
            if isinstance(issues, str):
                issues = []
            if isinstance(pull_requests, str):
                pull_requests = []
            markdown_path = report_generator.generate_raw_markdown_report(repo, issues, pull_requests)
            report_generator.generate_process_markdown_report(markdown_path)
