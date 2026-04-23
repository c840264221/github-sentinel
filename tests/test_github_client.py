import pytest
from app.services.github_client import GitHubClient
import requests


# ----------------------------
# Mock Response 类
# ----------------------------
class MockResponse:
    def __init__(self, json_data, status_code=200):
        self._json = json_data
        self.status_code = status_code

    def json(self):
        return self._json

    def raise_for_status(self):
        if self.status_code != 200:
            raise Exception("HTTP Error")


# ----------------------------
# fixture：创建 client
# ----------------------------
@pytest.fixture
def github_client():
    return GitHubClient(token="fake-token")


# ----------------------------
# 测试 fetch_issues（含过滤 PR）
# ----------------------------
def test_fetch_issues_filter_pr(github_client, mocker):
    fake_data = [
        {
            "title": "issue1",
            "html_url": "url1",
            "updated_at": "time1"
        },
        {
            "title": "pr1",
            "html_url": "url2",
            "updated_at": "time2",
            "pull_request": {}  # 这个应该被过滤
        }
    ]

    mocker.patch(
        "app.services.github_client.requests.get",
        return_value=MockResponse(fake_data)
    )

    result = github_client.fetch_issues("repo")

    assert len(result) == 1
    assert result[0]["title"] == "issue1"


# ----------------------------
# 测试 fetch_pull_requests
# ----------------------------
def test_fetch_pull_requests(github_client, mocker):
    fake_data = [
        {
            "title": "pr1",
            "html_url": "url1",
            "updated_at": "time1"
        }
    ]

    mocker.patch(
        "app.services.github_client.requests.get",
        return_value=MockResponse(fake_data)
    )

    result = github_client.fetch_pull_requests("repo")

    assert len(result) == 1
    assert result[0]["title"] == "pr1"


# ----------------------------
# 测试异常情况（网络错误）
# ----------------------------
def test_fetch_issues_exception(github_client, mocker):
    mocker.patch(
        "app.services.github_client.requests.get",
        side_effect=requests.exceptions.RequestException("network error")
    )

    result = github_client.fetch_issues("repo")

    assert result == []


# ----------------------------
# 测试 fetch_repo_updates（整合流程）
# ----------------------------
def test_fetch_repo_updates(github_client, mocker):
    mocker.patch(
        "app.services.github_client.GitHubClient.fetch_issues",
        return_value=[{"title": "issue"}]
    )

    mocker.patch(
        "app.services.github_client.GitHubClient.fetch_pull_requests",
        return_value=[{"title": "pr"}]
    )

    issues, prs = github_client.fetch_repo_updates("repo", since=None)

    assert len(issues) == 1
    assert len(prs) == 1