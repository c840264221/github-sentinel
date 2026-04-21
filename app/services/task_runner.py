from app.core.constants import SKIP
from app.core.logger import  LOG
from app.core.config import Settings
import os
from datetime import datetime


config = Settings()

class GithubTaskRunner:

    def __init__(self, github_service, report_generator, llm_client):
        self.github_service = github_service
        self.report_generator = report_generator
        self.llm_client = llm_client

    def run(self, task):
        try:
            print(f"🚀 Start task: {task.repo}")
            task.status = "running"
            LOG.info(f"<UNK> Start task: {task.repo}")

            # 1️⃣ 获取数据
            issues, prs = self.fetch(task)
            LOG.info(f"<UNK> Start fetching data: {task.repo}")

            # 👉 跳过逻辑
            if issues is SKIP and prs is SKIP:
                print(f"⏭ {task.repo} skipped")
                task.status = "skipped"
                LOG.info(f"<UNK> Skip task: {task.repo}")
                return task
            else:
                if issues is SKIP:
                    issues = []
                if prs is SKIP:
                    prs = []

            # 2️⃣ 生成原始 md
            raw_file = self.generate_md(task, issues, prs)
            task.raw_file = raw_file
            LOG.info(f"<UNK> generate_md: {task.repo}")

            # 3️⃣ LLM 总结
            summary = self.summarize(raw_file)

            # 4️⃣ 生成报告
            report_file = self.generate_report(raw_file, summary)
            task.report_file = report_file

            task.result = report_file
            task.status = "done"

            print(f"✅ GithubTask done: {task.repo}")

        except Exception as e:
            task.status = "failed"
            task.error = str(e)
            print(f"❌ GithubTask failed: {task.repo} | {e}")

        return task

    # -------------------------
    # steps
    # -------------------------

    def fetch(self, task):
        return self.github_service.fetch_repo_updates(
            repo=task.repo,
            since=task.since
        )

    def generate_md(self, task, issues, prs):
        return self.report_generator.generate_raw_markdown_report(
            repo_name=task.repo,
            issues=issues,
            pull_requests=prs
        )

    def summarize(self, raw_file):
        with open(raw_file, "r", encoding="utf-8") as f:
            content = f.read()

        return self.llm_client.generate_daily_report(content,config.github_prompt)

    def generate_report(self, raw_file, summary):
        return self.report_generator.generate_process_markdown_report(
            markdown_file_path=raw_file,
            markdown_file_content=summary
        )


class HNFetchTask:
    def __init__(self, hn_client, storage):
        self.hn_client = hn_client
        self.storage = storage

    def run(self):
        LOG.info("Start fetching Hacker News")

        titles = self.hn_client.fetch_top_stories()

        if not titles:
            LOG.warning("No data fetched")
            return

        self.storage.save(titles)

        LOG.info(f"Fetched {len(titles)} items")


class HNSummaryTask:
    def __init__(self, storage, llm, report_generator):
        self.storage = storage
        self.llm = llm
        self.report_generator = report_generator

    def run(self):
        data = self.storage.load()

        if not data:
            LOG.info("No data to summarize")
            return

        titles = [item["title"] for item in data]
        titles_str = "\n".join(titles)

        summary = self.llm.generate_daily_report(titles_str, config.hacker_news_prompt)
        today = datetime.now().date().isoformat()
        hn_report_file_name = ''.join([today, "_hn_report.md"])
        hn_report_path = os.path.join(config.HN_report_path, hn_report_file_name)
        self.report_generator.generate_process_markdown_report(markdown_file_content=summary, markdown_file_path=None,hn_report_path=hn_report_path)

        LOG.info("Summary report generated")