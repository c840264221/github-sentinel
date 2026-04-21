import requests
from bs4 import BeautifulSoup


class HackerNewsClient:
    URL = "https://news.ycombinator.com/"

    def fetch_top_stories(self, limit=5):
        response = requests.get(self.URL)
        soup = BeautifulSoup(response.text, "lxml")

        titles = []

        rows = soup.select("tr.athing")

        for row in rows[:limit]:
            title_tag = row.select_one(".titleline a")
            if title_tag:
                titles.append(title_tag.get_text(strip=True))

        return titles

if __name__ == "__main__":
    hacker_news_client = HackerNewsClient()
    a = hacker_news_client.fetch_top_stories()
    print(a)