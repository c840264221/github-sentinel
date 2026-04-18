import json
import os
from dotenv import load_dotenv


load_dotenv()
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REPOSITORY_DATA_FILE = os.path.join(BASE_DIR, "data", "subscriptions.json")

class Settings:
    def __init__(self):
        self.load_config()
    def load_config(self):
        self.github_token = os.getenv("GITHUB_TOKEN")
        self.default_repos = []
        with open(REPOSITORY_DATA_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            self.default_repos.extend(sub_data['repo_name'] for sub_data in data)
        self.update_interval = int(os.getenv("UPDATE_INTERVAL"))
        if self.update_interval:
            self.update_interval = int(self.update_interval)
        self.raw_reports_path = os.path.join(BASE_DIR, "reports", "raw")
