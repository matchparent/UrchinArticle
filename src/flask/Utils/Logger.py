import logging
import os
from logging.handlers import RotatingFileHandler
from .Env import config

DATE_FORMAT = "%Y/%m/%d %H:%M:%S "
LOG_FORMAT = "%(asctime)s-%(levelname)s-%(filename)s:%(lineno)d ===%(message)s"


def init_log():
    logging.basicConfig(level=config.log_level)

    # 当前文件（Logger.py）所在目录
    current_dir = os.path.dirname(__file__)
    # 进入上级目录（即 flask/）
    flask_dir = os.path.abspath(os.path.join(current_dir, ".."))
    # 构造 log 文件夹路径
    log_dir = os.path.join(flask_dir, "log")
    os.makedirs(log_dir, exist_ok=True)
    # 最终日志文件路径
    log_path = os.path.join(log_dir, "urchinArt.log")

    handler = RotatingFileHandler(log_path, maxBytes=1024 * 1024 * 200, backupCount=10)

    formatter = logging.Formatter(fmt=LOG_FORMAT, datefmt=DATE_FORMAT)
    handler.setFormatter(formatter)

    logging.getLogger().addHandler(handler)

    logging.info("==================================================================================")
