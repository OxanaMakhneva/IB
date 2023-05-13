import logging

_log_format = _log_format = f"%(asctime)s - [%(levelname)s] - %(name)s - (%(filename)s).%(funcName)s(%(lineno)d) - %(message)s"

class CustomFilter(logging.Filter):
    COLOR = {"DEBUG": "GREEN","INFO": "GREEN","WARNING": "YELLOW", "ERROR": "RED", "CRITICAL": "RED",}

    def filter(self, record):
        record.color = CustomFilter.COLOR[record.levelname]
        return True

def get_file_handler(file_name):
    file_handler = logging.FileHandler(file_name)
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(logging.Formatter(_log_format))
    return file_handler

def get_stream_handler():
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.INFO)
    stream_handler.setFormatter(logging.Formatter(_log_format))
    return stream_handler

def get_logger(name, file_name = "default_logger.txt"):
    logger = logging.getLogger(name)
    logger.addFilter(CustomFilter())
    logger.setLevel(logging.INFO)
    logger.addHandler(get_file_handler(file_name))
    logger.addHandler(get_stream_handler())
    return logger
