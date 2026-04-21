import os
from datetime import datetime
from app.core.config import Settings


config = Settings()
class ReportGenerator:
    def __init__(self):
        self.raw_reports_path = config.raw_reports_path
        self.processed_reports_path = config.processed_reports_path

    def generate_raw_markdown_report(self, repo_name, issues, pull_requests):
        # 创建 reports 目录
        os.makedirs(self.raw_reports_path, exist_ok=True)

        # 处理文件名
        safe_repo_name = repo_name.replace("/", "_")
        date_str = datetime.now().strftime("%Y-%m-%d")

        file_name = f"{safe_repo_name}_{date_str}.md"
        # file_path = os.path.join("reports", file_name)
        file_path = os.path.join(self.raw_reports_path, file_name)
        # 生成内容
        content = []

        content.append(f"# 📦 {repo_name} Updates ({date_str})\n")

        # Issues
        content.append("## 🐞 Issues\n")
        if not issues:
            content.append("No recent issues.\n")
        else:
            for issue in issues:
                content.append(f"- [{issue['title']}]({issue['url']})  ")
                content.append(f"  ⏱ Updated: {issue['updated_at']}\n")

        # Pull Requests
        content.append("\n## 🔀 Pull Requests\n")
        if not pull_requests:
            content.append("No recent pull requests.\n")
        else:
            for pr in pull_requests:
                content.append(f"- [{pr['title']}]({pr['url']})  ")
                content.append(f"  ⏱ Updated: {pr['updated_at']}\n")

        # 写入文件
        with open(file_path, "w", encoding="utf-8") as f:
            f.write("\n".join(content))

        print(f"📄 Report generated: {file_path}")

        return file_path

    def generate_process_markdown_report(self, markdown_file_content,markdown_file_path=None, hn_report_path=None):
        os.makedirs(self.processed_reports_path, exist_ok=True)
        report = markdown_file_content
        report_file_path = ''
        if markdown_file_path:
            report_file_name = os.path.basename(markdown_file_path)
            name_without_ext = os.path.splitext(report_file_name)[0]
            process_report_file_path = name_without_ext + "_report.md"
            report_file_path = os.path.join(self.processed_reports_path, process_report_file_path)
        # print(report_file_path)
        if hn_report_path:
            report_file_path = hn_report_path
        if len(report_file_path) == 0:
            return print(f"Not found report file path ")
        with open(report_file_path, 'w+', encoding="utf-8") as report_file:
            report_file.write(report)

        print(f"Generated report saved to {report_file_path}")
        return report_file_path
