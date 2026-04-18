import requests


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

    def fetch_issues(self, repo: str):
        url = f"{BASE_URL}/repos/{repo}/issues"
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        return response.json()
