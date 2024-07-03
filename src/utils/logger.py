import logging


class Logger:
    def __init__(self) -> None:
        self.logger = logging.getLogger(__name__)
        self.level = logging.INFO

        logging.basicConfig(
            filename=f'logs/system.log',
            level=logging.INFO
        )

    def info(self, text: str):
        self.logger.info(text)

    def error(self, text: str):
        self.logger.error(text)

    def warning(self, text: str):
        self.logger.warning(text)
