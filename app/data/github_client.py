import requests
from app.core.config import settings

BASE_URL = "https://api.github.com"

def _headers():
    return {
    "Authorization": f"Bearer {settings.GITHUB_TOKEN}",
    "Accept": "application/vnd.github+json",
}

def fetch_commits(repo: str):
    url = f"{BASE_URL}/repos/{repo}/commits"
    response = requests.get(url, headers=_headers())
    response.raise_for_status()
    return response.json()

def fetch_issues(repo: str):
    url = f"{BASE_URL}/repos/{repo}/issues"
    response = requests.get(url, headers=_headers())
    response.raise_for_status()
    return response.json()
