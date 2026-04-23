import os
import pytest
from app.services.report_generator import ReportGenerator


# ----------------------------
# fixture：使用临时目录
# ----------------------------
@pytest.fixture
def report_generator(tmp_path, mocker):
    # mock 配置路径
    mocker.patch(
        "app.services.report_generator.config.raw_reports_path",
        tmp_path / "raw"
    )
    mocker.patch(
        "app.services.report_generator.config.processed_reports_path",
        tmp_path / "processed"
    )

    return ReportGenerator()


# ----------------------------
# 测试 raw report 生成
# ----------------------------
def test_generate_raw_markdown(report_generator):
    issues = [
        {"title": "bug1", "url": "url1", "updated_at": "time1"}
    ]
    prs = [
        {"title": "pr1", "url": "url2", "updated_at": "time2"}
    ]

    file_path = report_generator.generate_raw_markdown_report(
        "repo", issues, prs
    )

    # 文件是否存在
    assert os.path.exists(file_path)

    # 内容是否正确
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    assert "repo" in content
    assert "bug1" in content
    assert "pr1" in content


# ----------------------------
# 测试空数据情况
# ----------------------------
def test_generate_raw_markdown_empty(report_generator):
    file_path = report_generator.generate_raw_markdown_report(
        "repo", [], []
    )

    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    assert "No recent issues" in content
    assert "No recent pull requests" in content


# ----------------------------
# 测试 processed report（从 markdown_file_path）
# ----------------------------
def test_generate_processed_report_with_path(report_generator, tmp_path):
    # 创建一个假的 markdown 文件
    fake_md = tmp_path / "test.md"
    fake_md.write_text("原始内容", encoding="utf-8")

    result_path = report_generator.generate_process_markdown_report(
        "处理后的内容",
        markdown_file_path=str(fake_md)
    )

    assert os.path.exists(result_path)

    with open(result_path, "r", encoding="utf-8") as f:
        content = f.read()

    assert content == "处理后的内容"


# ----------------------------
# 测试 processed report（hn_report_path）
# ----------------------------
def test_generate_processed_report_with_hn_path(report_generator, tmp_path):
    hn_path = tmp_path / "hn_report.md"

    result_path = report_generator.generate_process_markdown_report(
        "内容",
        hn_report_path=str(hn_path)
    )

    assert os.path.exists(result_path)


# ----------------------------
# 测试异常分支（没有路径）
# ----------------------------
def test_generate_processed_report_no_path(report_generator):
    result = report_generator.generate_process_markdown_report("内容")

    assert result is None