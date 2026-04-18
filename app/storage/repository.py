import json
import os
from app.core.config import REPOSITORY_DATA_FILE


class SubscriptionRepository:

    def __init__(self):
        os.makedirs("../data", exist_ok=True)

        if not os.path.exists(REPOSITORY_DATA_FILE):
            with open(REPOSITORY_DATA_FILE, "w") as f:
                json.dump([], f)

    def _load(self):
        with open(REPOSITORY_DATA_FILE, "r") as f:
            return json.load(f)

    def _save(self, data):
        with open(REPOSITORY_DATA_FILE, "w") as f:
            json.dump(data, f, indent=2)

    def get_all(self):
        return self._load()

    def add(self, repo_name, user="default"):
        data = self._load()

        # 去重
        if any(sub["repo_name"] == repo_name for sub in data):
            print("⚠️ Subscription already exists")
            return

        data.append({
            "repo_name": repo_name,
            "user": user
        })

        self._save(data)
        print(f"✅ Added subscription: {repo_name}")

    def remove(self, repo_name):
        data = self._load()

        new_data = [sub for sub in data if sub["repo_name"] != repo_name]

        if len(data) == len(new_data):
            print("⚠️ Subscription not found")
            return

        self._save(new_data)
        print(f"🗑️ Removed subscription: {repo_name}")