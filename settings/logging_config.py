import os
from datetime import datetime
import settings.params as p


class LoggingConfig:
    """
    Logging configuration class
    """

    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(LoggingConfig, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self, logging):
        if self._initialized:
            return
        self._initialized = True

        log_format = "%(asctime)s:\t" "%(levelname)s %(message)s"

        current_date = datetime.now().strftime("%Y_%m_%d")
        self.log_file = f"{current_date}.log"

        self.log = logging
        self.log.basicConfig(
            level=logging.INFO,
            format=log_format,
            filename=self.log_file,
            filemode="a",
        )

        # Adding console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        console_handler.setFormatter(logging.Formatter(log_format))
        self.log.getLogger().addHandler(console_handler)

    @staticmethod
    def print_header(header, logging):
        logging.info(80 * "-")
        logging.info((40 - int(len(header) / 2)) * " " + header)
        logging.info(80 * "-")
