import logging
import os
from datetime import datetime


def setup_logging(log_dir="logs", log_level=logging.DEBUG):
    os.makedirs(log_dir, exist_ok=True)
    log_filename = os.path.join(log_dir, f"trading_bot_{datetime.now().strftime('%Y%m%d')}.log")
    logger = logging.getLogger("trading_bot")
    logger.setLevel(log_level)
    if logger.handlers:
        return logger
    file_formatter = logging.Formatter(
        fmt="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    console_formatter = logging.Formatter(
        fmt="%(asctime)s | %(levelname)-8s | %(message)s",
        datefmt="%H:%M:%S",
    )
    file_handler = logging.FileHandler(log_filename, encoding="utf-8")
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(file_formatter)
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(console_formatter)
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    logger.info("Logging initialised → %s", log_filename)
    return logger


def get_logger(name):
    return logging.getLogger(f"trading_bot.{name}")
