import logging
import os
from datetime import datetime

# Set up log directory and files
log_dir = os.path.join(os.path.dirname(__file__), 'logs')
os.makedirs(log_dir, exist_ok=True)

# Log file paths
info_log_file = os.path.join(log_dir, f"scrapping_info_{datetime.now().strftime('%Y%m%d')}.log")
warning_log_file = os.path.join(log_dir, f"warning_{datetime.now().strftime('%Y%m%d')}.log")
error_log_file = os.path.join(log_dir, f"error_{datetime.now().strftime('%Y%m%d')}.log")

# Custom log levels
SCRAPPING_INFO_LEVEL = 25
logging.addLevelName(SCRAPPING_INFO_LEVEL, "SCRAPPING_INFO")

def scrapping_info(self, message, *args, **kws):
    if self.isEnabledFor(SCRAPPING_INFO_LEVEL):
        self._log(SCRAPPING_INFO_LEVEL, message, args, **kws)
logging.Logger.scrapping_info = scrapping_info

# Set up handlers
info_handler = logging.FileHandler(info_log_file, encoding='utf-8')
info_handler.setLevel(SCRAPPING_INFO_LEVEL)
info_handler.setFormatter(logging.Formatter('%(asctime)s [SCRAPPING_INFO] %(message)s'))

warning_handler = logging.FileHandler(warning_log_file, encoding='utf-8')
warning_handler.setLevel(logging.WARNING)
warning_handler.setFormatter(logging.Formatter('%(asctime)s [WARNING] %(message)s'))

error_handler = logging.FileHandler(error_log_file, encoding='utf-8')
error_handler.setLevel(logging.ERROR)
error_handler.setFormatter(logging.Formatter('%(asctime)s [ERROR] %(message)s'))

# Root logger setup
logging.basicConfig(level=logging.INFO, handlers=[info_handler, warning_handler, error_handler])

# Also log to console (optional)
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
console_handler.setFormatter(logging.Formatter('%(asctime)s [%(levelname)s] %(message)s'))
logging.getLogger().addHandler(console_handler)

def get_logger(name=None):
    return logging.getLogger(name)
