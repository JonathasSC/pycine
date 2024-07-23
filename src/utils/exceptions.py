from pydantic import ValidationError
from src.utils.printer import Printer
from src.utils.terminal import Terminal


class ExceptionsHandlers:
    def __init__(self) -> None:
        self.printer: Printer = Printer()
        self.terminal: Terminal = Terminal()

    def handle_validation_error(self, e: ValidationError):
        for error in e.errors():
            field = " -> ".join(map(str, error['loc']))
            self.printer.error(f'Erro no campo {field}, tente novamente', True)
        self.terminal.clear()
