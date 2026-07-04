from app.utils.config import load_config
from app.utils.logger import setup_logger
from app.pipeline.invoice_pipeline import InvoicePipeline
import undetected_chromedriver as uc



if __name__ == "__main__":
    logger = setup_logger()
    logger.info("Application started.")

    try:
        config = load_config("config.json")

        pipeline = InvoicePipeline(config)
        pipeline.run()

        logger.info("Scrapping finished successfully.")
        # Cleanup: OSError: [WinError 6] The handle is invalid
        uc.Chrome.__del__ = lambda self: None

    except Exception:
        logger.exception("Unhandled exception occurred.")
        raise