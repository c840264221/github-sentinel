from app.core.constants import SKIP
from app.core.logger import  get_logger


logger = get_logger(__name__)
class TaskRunner:

    def __init__(self, github_service, report_generator, llm_client):
        self.github_service = github_service
        self.report_generator = report_generator
        self.llm_client = llm_client

    def run(self, task):
        try:
            print(f"🚀 Start task: {task.repo}")
            task.status = "running"
            logger.info(f"<UNK> Start task: {task.repo}")

            # 1️⃣ 获取数据
            issues, prs = self.fetch(task)
            logger.info(f"<UNK> Start fetching data: {task.repo}")

            # 👉 跳过逻辑
            if issues is SKIP and prs is SKIP:
                print(f"⏭ {task.repo} skipped")
                task.status = "skipped"
                logger.info(f"<UNK> Skip task: {task.repo}")
                return task
            else:
                if issues is SKIP:
                    issues = []
                if prs is SKIP:
                    prs = []

            # 2️⃣ 生成原始 md
            raw_file = self.generate_md(task, issues, prs)
            task.raw_file = raw_file
            logger.info(f"<UNK> generate_md: {task.repo}")

            # 3️⃣ LLM 总结
            summary = self.summarize(raw_file)

            # 4️⃣ 生成报告
            report_file = self.generate_report(raw_file, summary)
            task.report_file = report_file

            task.result = report_file
            task.status = "done"

            print(f"✅ Task done: {task.repo}")

        except Exception as e:
            task.status = "failed"
            task.error = str(e)
            print(f"❌ Task failed: {task.repo} | {e}")

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

        return self.llm_client.generate_daily_report(content)

    def generate_report(self, raw_file, summary):
        return self.report_generator.generate_process_markdown_report(
            markdown_file_path=raw_file,
            markdown_file_content=summary
        )