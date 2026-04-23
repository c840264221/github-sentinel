import requests
from app.storage.repository import SubscriptionRepository
from app.services.verifiication import verify_md_exist, add_fetch_time
from app.core.logger import LOG
import os


class GitHubClient:
    subscription_repository = SubscriptionRepository()
    def __init__(self, token, base_url=None):
        self.token = token
        self.headers = {
            "Authorization": f"Bearer {self.token}",
            "Accept": "application/vnd.github+json",
        }
        self.base_url = base_url or os.getenv("GITHUB_BASE_URL")
    def fetch_repo_updates(self,repo, since):
        issues = self.fetch_issues(repo=repo, since=since)
        prs = self.fetch_pull_requests(repo=repo, since=since)
        return issues, prs

    def fetch_commits(self, repo: str):
        url = f"{self.base_url}/repos/{repo}/commits"
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        return response.json()

    @verify_md_exist(subscription_repository)
    def fetch_issues(self, repo: str, since=None):
        LOG.info(f"Fetching issues for {repo} since {since}")
        url = f"{self.base_url}/repos/{repo}/issues"
        params = {
            "state": "closed",
            "sort": "updated",
            # "direction": "desc",
        }
        if since:
            params["since"] = since
        try:
            resp = requests.get(url, headers=self.headers, params=params)
        except requests.exceptions.RequestException as e:
            LOG.error(e)
            return []
        resp.raise_for_status()

        data = resp.json()

        # ❗ 过滤掉 PR（issues API 会混入 PR）
        issues = [i for i in data if "pull_request" not in i]

        return [
            {
                "title": i["title"],
                "url": i["html_url"],
                "updated_at": i["updated_at"]
            }
            for i in issues
        ]

    @add_fetch_time(subscription_repository)
    @verify_md_exist(subscription_repository)
    def fetch_pull_requests(self, repo, since=None):
        url = f"{self.base_url}/repos/{repo}/pulls"
        params = {
            "state": "closed",
            "sort": "updated",
            # "direction": "desc",
        }
        if since:
            params["since"] = since
        try:
            resp = requests.get(url, headers=self.headers, params=params)
        except requests.exceptions.RequestException as e:
            LOG.error(e)
            return []
        resp.raise_for_status()

        data = resp.json()

        return [
            {
                "title": pr["title"],
                "url": pr["html_url"],
                "updated_at": pr["updated_at"]
            }
            for pr in data
        ]