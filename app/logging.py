import os
import sys

from loguru import logger


LOG_DIR = os.path.join(os.getcwd(), "logs")
os.makedirs(LOG_DIR, exist_ok=True)

logger.remove()
logger.add(sys.stdout, level="INFO", colorize=True, enqueue=True, backtrace=True, diagnose=True)
logger.add(os.path.join(LOG_DIR, "app.log"), rotation="10 MB", retention="10 days", level="INFO", enqueue=True)

def get_logger(name: str = "app"):
    return logger.bind(name=name)
