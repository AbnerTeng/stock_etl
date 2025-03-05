import logging
import os

OUTPUT_DIR = "/home/abner/stock_weekly_update"
os.makedirs(OUTPUT_DIR, exist_ok=True)


LOG_FILE = "/home/abner/logs/stock_etl.log"
os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)


logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)


def get_logger():
    logger = logging.getLogger("stock_etl")
    handler = logging.FileHandler(LOG_FILE)
    handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))
    logger.addHandler(handler)

    return logger


LOGGER = get_logger()
