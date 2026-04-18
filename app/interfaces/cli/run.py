from app.core.config import settings
from app.data.fetcher import fetch_repo
from app.services.summarizer import summarize
from app.storage.repository import SubscriptionRepository

def run():

    repo = SubscriptionRepository()
    repo.add("langchain-ai/langchain")
    # repo.add("openai/openai-python")
    print(repo.get_all())

    # repo.remove("openai/openai-python")

    # print(repo.get_all())

    for repo in settings.DEFAULT_REPOS:
        data = fetch_repo(repo)
        summary = summarize(data)

        print("=" * 40)
        print(summary)
