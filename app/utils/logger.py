import logging
from pathlib import Path


def setup_logger() -> logging.Logger:
    """
    Configure the application's logger.

    Creates the logs directory if it does not exist and writes all
    INFO and ERROR messages to logs/application.log.
    """

    logs_dir = Path("logs")
    logs_dir.mkdir(exist_ok=True)

    log_file = logs_dir / "application.log"

    logger = logging.getLogger("invoice_pipeline")

    # Prevent duplicate handlers if called more than once
    if logger.hasHandlers():
        return logger

    logger.setLevel(logging.INFO)

    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    file_handler = logging.FileHandler(log_file, encoding="utf-8")
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(formatter)

    logger.addHandler(file_handler)

    return logger