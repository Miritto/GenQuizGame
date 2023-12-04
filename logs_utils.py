import logging
import os
from logging.handlers import TimedRotatingFileHandler
from typing import Optional


class LoggerCreator:
    def __init__(self, logs_dir):
        self.logs_dir = logs_dir
        if not os.path.exists(self.logs_dir):
            os.mkdir(self.logs_dir)

    def create_rotating_logger(self, log_name,
                               log_dir: Optional[str] = '',
                               level=logging.INFO):
        logger = logging.getLogger(log_name)
        logger.setLevel(level)

        logs_path = os.path.join(self.logs_dir, log_dir)
        if not os.path.exists(logs_path):
            os.mkdir(logs_path)

        formatter = logging.Formatter('%(asctime)s UTC %(levelname)s %(message)s',
                                      datefmt="%d-%m-%Y %H:%M:%S")

        info_handler = TimedRotatingFileHandler(
            os.path.join(logs_path, f"{log_name}_info.log"),
            when="midnight",
            interval=1,
            utc=True,
            encoding='utf-8',
        )
        info_handler.setLevel(logging.INFO)
        info_handler.suffix = "%Y-%m-%d"

        error_handler = TimedRotatingFileHandler(
            os.path.join(logs_path, f"{log_name}_error.log"),
            when="midnight",
            interval=1,
            utc=True,
            encoding='utf-8',
        )
        error_handler.setLevel(logging.ERROR)
        error_handler.suffix = "%Y-%m-%d"

        info_handler.setFormatter(formatter)
        error_handler.setFormatter(formatter)

        logger.addHandler(info_handler)
        logger.addHandler(error_handler)

        return logger
