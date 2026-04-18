import json
import os
from dotenv import load_dotenv


load_dotenv()
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REPOSITORY_DATA_FILE = os.path.join(BASE_DIR, "data", "subscriptions.json")

class Settings:
    GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
    DEFAULT_REPOS = []
    with open(REPOSITORY_DATA_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)
        # print(data)
        DEFAULT_REPOS.extend(sub_data['repo_name'] for sub_data in data)
    # print(DEFAULT_REPOS)

settings = Settings()
