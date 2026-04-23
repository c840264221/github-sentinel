import pytest
from app.services.hacker_news_client import HackerNewsClient


# ----------------------------
# Mock Response
# ----------------------------
class MockResponse:
    def __init__(self, text):
        self.text = text


# ----------------------------
# fixture
# ----------------------------
@pytest.fixture
def hn_client():
    return HackerNewsClient()


# ----------------------------
# 测试正常解析
# ----------------------------
def test_fetch_top_stories(hn_client, mocker):
    fake_html = """
    <html>
        <body>
            <tr class="athing">
                <td class="titleline">
                    <a>Title 1</a>
                </td>
            </tr>
            <tr class="athing">
                <td class="titleline">
                    <a>Title 2</a>
                </td>
            </tr>
        </body>
    </html>
    """

    mocker.patch(
        "app.services.hacker_news_client.requests.get",
        return_value=MockResponse(fake_html)
    )

    result = hn_client.fetch_top_stories(limit=2)

    assert len(result) == 2
    assert result[0] == "Title 1"
    assert result[1] == "Title 2"


# ----------------------------
# 测试 limit 限制
# ----------------------------
def test_fetch_top_stories_limit(hn_client, mocker):
    fake_html = """
    <html>
        <body>
            <tr class="athing"><td class="titleline"><a>A</a></td></tr>
            <tr class="athing"><td class="titleline"><a>B</a></td></tr>
            <tr class="athing"><td class="titleline"><a>C</a></td></tr>
        </body>
    </html>
    """

    mocker.patch(
        "app.services.hacker_news_client.requests.get",
        return_value=MockResponse(fake_html)
    )

    result = hn_client.fetch_top_stories(limit=1)

    assert len(result) == 1
    assert result[0] == "A"


# ----------------------------
# 测试 HTML 结构异常
# ----------------------------
def test_fetch_top_stories_empty(hn_client, mocker):
    fake_html = "<html><body>No data</body></html>"

    mocker.patch(
        "app.services.hacker_news_client.requests.get",
        return_value=MockResponse(fake_html)
    )

    result = hn_client.fetch_top_stories()

    assert result == []