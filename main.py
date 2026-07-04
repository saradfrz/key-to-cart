from app.utils.config import load_config
from app.utils.logger import setup_logger
from app.pipeline.invoice_pipeline import InvoicePipeline
import undetected_chromedriver as uc

import os
import shutil



if __name__ == "__main__":
    # Setup the environment and directories
    config = load_config("config.json")
    dirs = [config.dir.output_html, config.dir.logs]
    for directory in dirs:
        if os.path.exists(directory):
            shutil.rmtree(directory)
        os.makedirs(directory, exist_ok=True)

    logger = setup_logger()
    logger.info("Application started.")

    try:
        pipeline = InvoicePipeline(config)
        pipeline.run()

        logger.info("Scrapping finished successfully.")
        # Cleanup: OSError: [WinError 6] The handle is invalid
        uc.Chrome.__del__ = lambda self: None

    except Exception:
        logger.exception("Unhandled exception occurred.")
        raise