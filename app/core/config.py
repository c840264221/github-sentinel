import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
    DEFAULT_REPOS = [
        "openai/openai-python",
        "langchain-ai/langchain",
    ]

settings = Settings()
