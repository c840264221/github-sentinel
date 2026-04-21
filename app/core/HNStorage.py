import json
from datetime import datetime
from app.core.config import Settings
from pathlib import Path


config = Settings()
HN_storage_json_path = config.HN_storage_json_path

class HNStorage:
    FILE = Path(HN_storage_json_path)

    def save(self, titles):
        data = self.load()
        existing = [item['title'] for item in data]
        for title in titles:
            if title not in existing:
                data.append({
                    "title": title,
                    "time": datetime.now().isoformat(),
                    "count": 1
                })
            else:
                for item in data:
                    if item['title'] == title:
                        # item['count'] = str(int(item['count']) + 1)
                        item['count'] += 1
                        break

        self.FILE.write_text(json.dumps(data, indent=2))

    def load(self):
        if not self.FILE.exists():
            return []
        return json.loads(self.FILE.read_text())