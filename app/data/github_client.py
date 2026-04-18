import requests
from datetime import datetime, timedelta, date


BASE_URL = "https://api.github.com"


class GitHubClient:
    def __init__(self, token):
        self.token = token
        self.headers = {
            "Authorization": f"Bearer {self.token}",
            "Accept": "application/vnd.github+json",
        }

    def fetch_commits(self, repo: str):
        url = f"{BASE_URL}/repos/{repo}/commits"
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        return response.json()

    def fetch_issues(self, repo: str, since=None):
        url = f"{BASE_URL}/repos/{repo}/issues"
        params = {
            "state": "closed",
            "sort": "updated",
            "direction": "desc",
        }
        if since:
            params["since"] = since

        resp = requests.get(url, headers=self.headers, params=params)
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

    def fetch_pull_requests(self, repo, since=None):
        url = f"{BASE_URL}/repos/{repo}/pulls"
        params = {
            "state": "closed",
            "sort": "updated",
            "direction": "desc",
        }
        if since:
            params["since"] = since
        resp = requests.get(url, headers=self.headers, params=params)
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