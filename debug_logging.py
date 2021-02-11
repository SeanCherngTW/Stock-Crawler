import os
import logging
from logging import handlers

model_name = 'stock_crawler'
logFilePath = "log/" + model_name + ".log"
dstDir = 'log'

if not os.path.exists(dstDir):
    os.mkdir(dstDir)


class DebugLog:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        self.logger = self.logger_initialize()
        self.logger.propagate = False
        self.model_name = model_name

    def logger_initialize(self):
        # init logger
        logger = logging.getLogger(model_name)
        logger.setLevel(logging.INFO)
        formatter = logging.Formatter('[%(asctime)s] - [%(name)s] - [%(filename)s] - %(levelname)s - %(message)s')
        fh = handlers.RotatingFileHandler(
            filename=logFilePath, maxBytes=50 * 1024 * 1024, backupCount=1, encoding="utf-8",
        )
        fh.setLevel(logging.INFO)
        fh.setFormatter(formatter)
        logger.addHandler(fh)
        ch = logging.StreamHandler()
        ch.setLevel(logging.INFO)
        ch.setFormatter(formatter)
        logger.addHandler(ch)

        return logger
