import logging
import os


class Logger:
    def __init__(self) -> None:
        self.logger = logging.getLogger(__name__)
        self.level = logging.INFO

        log_directory = 'logs'
        log_filename = 'system.log'

        os.makedirs(log_directory, exist_ok=True)

        logging.basicConfig(
            filename=os.path.join(log_directory, log_filename),
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )

    def info(self, text: str) -> None:
        self.logger.info(text)

    def error(self, text: str) -> None:
        self.logger.error(text)

    def warning(self, text: str) -> None:
        self.logger.warning(text)
