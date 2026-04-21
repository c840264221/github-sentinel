import json
import os
from dotenv import load_dotenv


load_dotenv()
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REPOSITORY_DATA_FILE = os.path.join(BASE_DIR, "data", "subscriptions.json")
config_file_path = os.path.join(BASE_DIR, "data", "config.json")

class Settings:
    def __init__(self):
        self.load_config()

    def load_config(self):
        with open(REPOSITORY_DATA_FILE, "r") as x:
            repository_data = json.load(x)
            self.default_repos = [repo_data["repo_name"] for repo_data in repository_data]
        with open(config_file_path, 'r') as f:
            config = json.load(f)
            self.github_token = os.getenv("GITHUB_TOKEN")
            self.update_interval = config.get("update_interval")

            self.raw_reports_path = os.path.join(BASE_DIR, "reports", "raw")
            self.processed_reports_path = os.path.join(BASE_DIR, "reports", "process")
            email_config = config.get("email")
            self.email_smtp_server = email_config.get("smtp_server")
            self.email_smtp_port = email_config.get("smtp_port")
            self.email_from = email_config.get("from")
            self.email_to = email_config.get("to")
            self.email_auth_code = os.getenv("QQ_EMAIL_AUTH_CODE", email_config.get("auth_code"))
