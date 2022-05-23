import logging

from commmons import get_file_handler


def get_mpsafe_logger(config: dict):
    logger = logging.getLogger("copier")
    if not logger.hasHandlers():
        logger.setLevel(logging.INFO)
        logger.addHandler(logging.StreamHandler())
        logger.addHandler(get_file_handler(config["basic"]["log_path"], multiprocessing_safe=True))
    return logger
