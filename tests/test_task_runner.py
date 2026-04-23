import pytest

class FakeTask:
    def __init__(self):
        self.repo = "repo"
        self.since = None
        self.status = None
        self.raw_file = None
        self.report_file = None
        self.result = None
        self.error = None

def test_github_task_success(mocker):
    from app.services.task_runner import GithubTaskRunner

    # mock 依赖
    github_service = mocker.Mock()
    report_generator = mocker.Mock()
    llm_client = mocker.Mock()

    # mock 返回值
    github_service.fetch_repo_updates.return_value = (["issue"], ["pr"])
    report_generator.generate_raw_markdown_report.return_value = "raw.md"
    llm_client.generate_daily_report.return_value = "summary"
    report_generator.generate_process_markdown_report.return_value = "report.md"

    runner = GithubTaskRunner(github_service, report_generator, llm_client)

    # mock掉runner的summarize方法，让他直接返回数据，跳过真实的文件写入功能
    mocker.patch.object(runner, "summarize", return_value="summary")

    task = FakeTask()

    result = runner.run(task)

    assert result.status == "done"
    assert result.raw_file == "raw.md"
    assert result.report_file == "report.md"

    github_service.fetch_repo_updates.assert_called_once()
    report_generator.generate_raw_markdown_report.assert_called_once()

    # 因为mock掉了 summarize方法 所以llm的generate_daily_report方法不进行测试
    # llm_client.generate_daily_report.assert_called_once()

def test_github_task_skip(mocker):
    from app.services.task_runner import GithubTaskRunner
    from app.core.constants import SKIP

    github_service = mocker.Mock()
    report_generator = mocker.Mock()
    llm_client = mocker.Mock()

    github_service.fetch_repo_updates.return_value = (SKIP, SKIP)

    runner = GithubTaskRunner(github_service, report_generator, llm_client)
    task = FakeTask()

    result = runner.run(task)

    assert result.status == "skipped"

def test_github_task_exception(mocker):
    from app.services.task_runner import GithubTaskRunner

    github_service = mocker.Mock()
    report_generator = mocker.Mock()
    llm_client = mocker.Mock()

    github_service.fetch_repo_updates.side_effect = Exception("boom")

    runner = GithubTaskRunner(github_service, report_generator, llm_client)
    task = FakeTask()

    result = runner.run(task)

    assert result.status == "failed"
    assert "boom" in result.error

def test_hn_fetch_task(mocker):
    from app.services.task_runner import HNFetchTask

    hn_client = mocker.Mock()
    storage = mocker.Mock()

    hn_client.fetch_top_stories.return_value = ["A", "B"]

    task = HNFetchTask(hn_client, storage)
    task.run()

    storage.save.assert_called_once_with(["A", "B"])

def test_hn_fetch_empty(mocker):
    from app.services.task_runner import HNFetchTask

    hn_client = mocker.Mock()
    storage = mocker.Mock()

    hn_client.fetch_top_stories.return_value = []

    task = HNFetchTask(hn_client, storage)
    task.run()

    storage.save.assert_not_called()

def test_hn_summary_task(mocker):
    from app.services.task_runner import HNSummaryTask

    storage = mocker.Mock()
    llm = mocker.Mock()
    report_generator = mocker.Mock()

    storage.load.return_value = [
        {"title": "A"},
        {"title": "B"}
    ]

    llm.generate_daily_report.return_value = "summary"

    task = HNSummaryTask(storage, llm, report_generator)
    task.run()

    llm.generate_daily_report.assert_called_once()
    report_generator.generate_process_markdown_report.assert_called_once()