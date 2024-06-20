from pydantic import ValidationError
from src.utils.printer import Printer


class ExceptionsHandlers:
    def __init__(self) -> None:
        self.printer: Printer = Printer()

    def handle_validation_error(self, e: ValidationError):
        for error in e.errors():
            field = " -> ".join(map(str, error['loc']))
            message = error['msg']
            self.printer.error(f'Error in {field}: {message}', True)
