import logging
from datetime import datetime

def setup_logging():
    log_filename = datetime.now().strftime("app_%Y-%m-%d.log")

    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s - %(levelname)s - %(message)s',
        filename=log_filename,
        filemode='a'
    )