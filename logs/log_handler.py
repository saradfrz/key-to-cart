import logging
import os

# Define custom log level for scraping info
SCRAPING_INFO_LEVEL = 25
logging.addLevelName(SCRAPING_INFO_LEVEL, "SCRAPING_INFO")

def scraping_info(self, message: str, *args, **kwargs) -> None:
    """
    Log 'message' with level 'SCRAPING_INFO_LEVEL'.
    """
    if self.isEnabledFor(SCRAPING_INFO_LEVEL):
        self._log(SCRAPING_INFO_LEVEL, message, args, **kwargs)

# Inject custom level method into Logger class
logging.Logger.scraping_info = scraping_info

def setup_logger(name: str, level: int = logging.DEBUG) -> logging.Logger:
    """
    Set up a logger with custom levels and file handlers for:
    - ERROR -> logs/error.log
    - WARNING -> logs/warning.log
    - SCRAPING_INFO -> logs/scraping.log

    All handlers use UTF-8 encoding to support special characters like 'ç', 'ã', etc.
    """
    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.propagate = False  # Prevent log duplication in root logger

    log_dir = "logs"
    os.makedirs(log_dir, exist_ok=True)

    # Unified log formatter
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    # UTF-8 encoded handlers
    error_handler = logging.FileHandler(os.path.join(log_dir, 'error.log'), encoding='utf-8')
    error_handler.setLevel(logging.ERROR)
    error_handler.setFormatter(formatter)

    warning_handler = logging.FileHandler(os.path.join(log_dir, 'warning.log'), encoding='utf-8')
    warning_handler.setLevel(logging.WARNING)
    warning_handler.setFormatter(formatter)

    scraping_handler = logging.FileHandler(os.path.join(log_dir, 'scraping.log'), encoding='utf-8')
    scraping_handler.setLevel(SCRAPING_INFO_LEVEL)
    scraping_handler.setFormatter(formatter)

    # Avoid duplicate handlers
    if not logger.handlers:
        logger.addHandler(error_handler)
        logger.addHandler(warning_handler)
        logger.addHandler(scraping_handler)

    return logger
