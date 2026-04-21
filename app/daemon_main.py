import time
import json
import sys
import signal
import os
from datetime import datetime, timedelta

import schedule

from app.services.github_client import GitHubClient
from app.services.report_generator import ReportGenerator
from app.services.llm.ollama_client import OllamaClient
from app.services.task_runner import TaskRunner
from app.domain.task import Task
from app.core.logger import LOG
from app.core.config import Settings, REPOSITORY_DATA_FILE
from app.services.notification.email_sender import EmailSender


# 设置停止程序标识符
shutdown_flag = False

# -------------------------
# 初始化依赖
# -------------------------
config = Settings()
github_token = config.github_token
github_client = GitHubClient(github_token)
report_generator = ReportGenerator()
llm_client = OllamaClient()

runner = TaskRunner(
    github_client,
    report_generator,
    llm_client
)

email_sender = EmailSender(config.email_smtp_server, config.email_smtp_port, config.email_from, config.email_auth_code)

# -------------------------
# 优雅退出
# -------------------------
def graceful_shutdown(signum, frame):
    global shutdown_flag
    LOG.info("[优雅退出] 接收到终止信号，准备关闭...")
    shutdown_flag = True

# -------------------------
# 读取订阅仓库
# -------------------------
def load_repos():
    try:
        with open(REPOSITORY_DATA_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
        return [item["repo_name"] for item in data]
    except Exception as e:
        LOG.error(f"Failed to load subscriptions: {e}")
        return []


# -------------------------
# 定时任务逻辑
# -------------------------
def run_scheduled_task():
    LOG.info("Scheduled task started")

    repos = load_repos()

    if not repos:
        LOG.warning("No repositories found")
        return

    for repo in repos:
        try:
            since_date = datetime.now() - timedelta(days=1)

            task = Task(repo=repo, since=since_date)

            LOG.info(f"Running task for {repo}")
            result = runner.run(task)

            if result.status == "done":
                LOG.info(f"{repo} done")
                email_subject = ''.join([result.repo,datetime.now().date().isoformat(),"总结报告"])
                report_file_path = os.path.join(config.processed_reports_path, result.report_file)
                with open(report_file_path, "r", encoding="utf-8") as f:
                    content = f.read()
                email_content = content
                email_sender.send_email(config.email_to, email_subject, email_content)
            elif result.status == "skipped":
                LOG.info(f"{repo} skipped")
            else:
                LOG.error(f"{repo} failed: {result.error}")

        except Exception as e:
            LOG.exception(f"Error running task for {repo}: {e}")

    LOG.info("Scheduled task finished")


# -------------------------
# 主循环
# -------------------------
def main():
    signal.signal(signal.SIGTERM, graceful_shutdown)
    signal.signal(signal.SIGINT, graceful_shutdown)  # Ctrl+C

    LOG.info("Daemon process started")

    run_scheduled_task()

    # 每天固定时间执行（推荐 ⭐）
    schedule.every().day.at("09:00").do(run_scheduled_task)

    # 测试用（每分钟）
    # schedule.every(1).minutes.do(run_scheduled_task)

    try:
        while not shutdown_flag:
            schedule.run_pending()
            time.sleep(5)
    except Exception as e:
        LOG.error(f"主进程发生异常: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()