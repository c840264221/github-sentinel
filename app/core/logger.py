import sys
import os
from loguru import logger

# 防止重复初始化（很重要）
if not logger._core.handlers:

    log_dir = "logs"
    os.makedirs(log_dir, exist_ok=True)

    log_format = "{time:YYYY-MM-DD HH:mm:ss} | {level} | {module}:{function}:{line} - {message}"

    # 清除默认 handler
    logger.remove()

    # 控制台
    logger.add(
        sys.stdout,
        level="DEBUG",
        format=log_format,
        colorize=True
    )

    # 文件
    logger.add(
        os.path.join(log_dir, "app.log"),
        level="DEBUG",
        format=log_format,
        rotation="1 MB",
        encoding="utf-8"
    )

# 对外暴露统一入口
LOG = logger