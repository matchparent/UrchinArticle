import logging
from logging.handlers import RotatingFileHandler
from .Env import config

DATE_FORMAT = "%Y/%m/%d %H:%M:%S "
LOG_FORMAT = "%(asctime)s-%(levelname)s-%(filename)s:%(lineno)d ===%(message)s"


def init_log():
    logging.basicConfig(level=config.log_level)
    handler = RotatingFileHandler("../log/urchinArt.log", maxBytes=1024 * 1024 * 200, backupCount=10)

    formatter = logging.Formatter(fmt=LOG_FORMAT, datefmt=DATE_FORMAT)
    handler.setFormatter(formatter)

    logging.getLogger().addHandler(handler)

    logging.info("==================================================================================")
