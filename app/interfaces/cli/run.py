from app.core.config import settings
from app.data.fetcher import fetch_repo
from app.services.summarizer import summarize

def run():
    for repo in settings.DEFAULT_REPOS:
        data = fetch_repo(repo)
        summary = summarize(data)

        print("=" * 40)
        print(summary)