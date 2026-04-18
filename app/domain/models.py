from typing import List, Dict

class RepoData:
    def __init__(self, name: str, commits: List[Dict], issues: List[Dict]):
        self.name = name
        self.commits = commits
        self.issues = issues

class Report:
    def __init__(self, repo: str, summary: str):
        self.repo = repo
        self.summary = summary
