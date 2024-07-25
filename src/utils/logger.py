import logging


class Logger:
    def __init__(self) -> None:
        self.logger = logging.getLogger(__name__)
        self.level = logging.INFO

        logging.basicConfig(
            filename='logs/system.log',
            level=logging.INFO
        )

    def info(self, text: str) -> None:
        self.logger.info(text)

    def error(self, text: str) -> None:
        self.logger.error(text)

    def warning(self, text: str) -> None:
        self.logger.warning(text)
