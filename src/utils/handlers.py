from pydantic import ValidationError
from src.utils.printer import Printer
from src.utils.terminal import Terminal


class Handlers:
    def __init__(self) -> None:
        self.printer: Printer = Printer()
        self.terminal: Terminal = Terminal()

    def handle_validation_error(self, e: ValidationError) -> None:
        for error in e.errors():
            field = " -> ".join(map(str, error['loc']))
            self.printer.error(f'Erro no campo {field}, tente novamente', True)
        self.terminal.clear()

    def handle_no_sessions_available(self) -> None:
        self.printer.warning(
            text="Nenhuma sessão disponível.",
            clear=True)

    def handle_no_tickets(self) -> None:
        self.printer.warning(
            text="Nenhum ticket comprado até o momento.",
            clear=True)
