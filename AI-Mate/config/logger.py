import logging
from pathlib import Path


def setup_logger():

    log_dir = Path("logs")

    log_dir.mkdir(
        exist_ok=True
    )


    logging.basicConfig(
        level=logging.INFO,
        format=
        "%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        handlers=[
            logging.FileHandler(
                log_dir / "ai_mate.log",
                encoding="utf-8"
            ),
            logging.StreamHandler()
        ]
    )


def get_logger(name):

    return logging.getLogger(name)