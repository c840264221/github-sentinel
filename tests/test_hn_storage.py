import pytest
from app.core.HNStorage import HNStorage
import json


# ----------------------------
# fixture：使用临时文件
# ----------------------------
@pytest.fixture
def storage(tmp_path, mocker):
    file_path = tmp_path / "hn.json"

    # mock FILE 路径
    mocker.patch("app.core.HNStorage.HNStorage.FILE", file_path)

    return HNStorage()

def test_load_empty(storage):
    data = storage.load()
    assert data == []

def test_hn_storage_save_new(storage):
    storage.save(["tittle1", "tittle2"])

    data = storage.load()

    assert len(data) == 2
    assert data[0]["title"] == "tittle1"
    assert data[0]["count"] == 1
    assert data[1]["title"] == "tittle2"

def test_save_mixed_titles(storage):
    storage.save(["tittle1", "tittle2"])
    storage.save(["tittle3", "tittle1"])

    data = storage.load()

    titles = {item["title"]: item for item in data}

    assert titles["tittle1"]["count"] == 2
    assert titles["tittle2"]["count"] == 1
    assert titles["tittle3"]["count"] == 1

def test_file_written(storage):
    storage.save(["tittle1", "tittle2"])

    raw = storage.FILE.read_text()
    data = json.loads(raw)

    assert data[0]["title"] == "tittle1"
    assert data[1]["title"] == "tittle2"