import gradio as gr
import json
from datetime import datetime, timedelta
import os

from app.domain.task import GithubTask
from app.services.task_runner import GithubTaskRunner
from app.services.github_client import GitHubClient
from app.services.report_generator import ReportGenerator
from app.services.llm.ollama_client import OllamaClient
from app.core.config import Settings, REPOSITORY_DATA_FILE



# -------------------------
# 初始化依赖（复用你现有结构）
# -------------------------
config = Settings()
processed_reports_path = config.processed_reports_path
github_token = config.github_token
repository_data_filename = REPOSITORY_DATA_FILE
github_client = GitHubClient(github_token)
report_generator = ReportGenerator()
llm_client = OllamaClient()

runner = GithubTaskRunner(
    github_client,
    report_generator,
    llm_client
)


# -------------------------
# 读取订阅仓库（从json）
# -------------------------
def load_repos():
    if not os.path.exists(repository_data_filename):
        return []

    with open(repository_data_filename, "r", encoding="utf-8") as f:
        data = json.load(f)

    # 假设结构：[{ "repo_name": "xxx" }]
    return [item["repo_name"] for item in data]

def get_existing_report(repo, since_date):
    # 文件名规则（按你现在的命名来）
    filename = f"{repo.replace('/', '_')}_{since_date}_report.md"

    file_path = os.path.join(processed_reports_path, filename)
    if os.path.exists(file_path):
        return file_path

    return None


# -------------------------
# 核心执行逻辑
# -------------------------
def run_task(repo, days):
    if not repo:
        return "❌ 请先选择仓库", "", None

    since_date = datetime.now() - timedelta(days=int(days))

    task = GithubTask(repo=repo, since=since_date)
    result = runner.run(task)

    # 处理状态
    if result.status == "failed":
        return f"❌ Failed:\n{result.error}", "", None

    if result.status == "skipped":
        today_time = datetime.now().date().isoformat()

        existing_file = get_existing_report(repo, today_time)
        if existing_file:
            with open(existing_file, "r", encoding="utf-8") as f:
                content = f.read()

            filename = os.path.basename(existing_file)

            return (
                f"⏭ 已跳过（使用已有报告）\n\n{content}",
                filename,
                existing_file
            )

        return "⏭ 已跳过，但未找到历史报告", "", None

    # 读取报告内容
    if result.report_file and os.path.exists(result.report_file):
        with open(result.report_file, "r", encoding="utf-8") as f:
            content = f.read()

        filename = os.path.basename(result.report_file)
        return content, filename, result.report_file

    return "⚠️ 未生成报告", "", None


# -------------------------
# 清空（恢复默认）
# -------------------------
def clear_inputs():
    return None, 1, "", "", None


# -------------------------
# UI
# -------------------------
with gr.Blocks() as demo:
    gr.Markdown("# 🚀 GitHub Sentinel")

    with gr.Row():

        # =====================
        # 左侧
        # =====================
        with gr.Column(scale=1):

            repo_dropdown = gr.Dropdown(
                choices=load_repos(),
                label="选择订阅仓库"
            )

            days_slider = gr.Slider(
                minimum=1,
                maximum=30,
                step=1,
                value=1,
                label="最近多少天"
            )

            with gr.Row():
                clear_btn = gr.Button("Clear")
                submit_btn = gr.Button("Submit")

        # =====================
        # 右侧
        # =====================
        with gr.Column(scale=2):

            markdown_output = gr.Markdown(label="报告内容")

            file_name = gr.Textbox(
                label="文件名",
                interactive=False
            )

            download_file = gr.File(label="下载文件")

            download_btn = gr.Button("Download")

    # -------------------------
    # 事件绑定
    # -------------------------

    # 提交
    submit_btn.click(
        fn=run_task,
        inputs=[repo_dropdown, days_slider],
        outputs=[markdown_output, file_name, download_file]
    )

    # 清空
    clear_btn.click(
        fn=clear_inputs,
        outputs=[repo_dropdown, days_slider, markdown_output, file_name, download_file]
    )

    # 下载按钮（其实 File 已支持点击下载，这里只是触发刷新）
    download_btn.click(
        fn=lambda f: f,
        inputs=download_file,
        outputs=download_file
    )


if __name__ == "__main__":
    demo.launch()