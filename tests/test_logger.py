def test_logger_basic():
    from app.core.logger import LOG

    # 不报错即可
    LOG.info("test log")

    assert LOG is not None

# 测试文件是否被创建
def test_log_file_creation(tmp_path, mocker):
    # mock 日志目录
    mocker.patch("app.core.logger.os.path.join", return_value=str(tmp_path / "app.log"))
    mocker.patch("app.core.logger.os.makedirs")

    # 关键：重新加载模块
    import importlib
    import app.core.logger

    importlib.reload(app.core.logger)

    LOG = app.core.logger.LOG

    LOG.info("test logger")

    assert (tmp_path / "app.log").exists()

def test_logger_handlers():
    from app.core.logger import LOG

    handlers = LOG._core.handlers

    # 至少应该有2个 handler（console + file）
    assert len(handlers) >= 2

# 测试防止重复初始化
def test_logger_no_duplicate_handlers():
    from app.core.logger import LOG

    handlers_before = len(LOG._core.handlers)

    # 再 import 一次
    from app.core.logger import LOG as LOG2

    handlers_after = len(LOG2._core.handlers)

    assert handlers_before == handlers_after