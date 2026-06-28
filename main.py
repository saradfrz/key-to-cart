from app.utils.config import load_config
from app.utils.logger import setup_logger
from app.pipeline.invoice_pipeline import InvoicePipeline


if __name__ == "__main__":
    logger = setup_logger()
    logger.info("Application started.")

    try:
        config = load_config("config.json")

        pipeline = InvoicePipeline(config)
        pipeline.run()

        logger.info("Application finished successfully.")

    except Exception:
        logger.exception("Unhandled exception occurred.")
        raise