import os
from datetime import datetime
from app.core.config import Settings


config = Settings()
def generate_markdown_report(repo_name, issues, pull_requests):
    raw_reports_path = config.raw_reports_path
    # 创建 reports 目录
    os.makedirs(raw_reports_path, exist_ok=True)

    # 处理文件名
    safe_repo_name = repo_name.replace("/", "_")
    date_str = datetime.now().strftime("%Y-%m-%d")

    file_name = f"{safe_repo_name}_{date_str}.md"
    # file_path = os.path.join("reports", file_name)
    file_path = os.path.join(raw_reports_path, file_name)
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