from app.core.config import Settings
from app.services.github_client import GitHubClient
from app.services.report_generator import ReportGenerator
from datetime import datetime, timedelta
from app.services.llm.ollama_client import OllamaClient
from app.domain.task import GithubTask
from app.services.task_runner import GithubTaskRunner



settings = Settings()
def run():

    llm_client = OllamaClient()
    report_generator = ReportGenerator()

    since = datetime.now() - timedelta(days=1)

    for repo in settings.default_repos:
        task = GithubTask(repo=repo, since=since)

        runner = GithubTaskRunner(
            GitHubClient(settings.github_token),
            report_generator,
            llm_client
        )

        result = runner.run(task)

        print(f"GithubTask status: {result.status}")