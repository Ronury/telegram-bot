import sys
from loguru import logger

from src.core import config


log_level = "DEBUG"
log_format = "<green>{time:YYYY-MM-DD HH:mm:ss.SSS zz}</green> | <level>{level: <8}</level> | <yellow>Line {line: >4} ({file}):</yellow> <b>{message}</b>"
logger.add(config.LOGS_PATH / "events.log", level=log_level, format=log_format, colorize=False, backtrace=True, diagnose=True)
