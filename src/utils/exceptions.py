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

    def handle_admin_options(self, option: int):
        if option == 1:
            self.list_movies_in_playing()

        elif option == 2:
            self.show_my_tickets()
            self.start()

        elif option == 3:
            self.process_purchase()

        elif option == 4:
            self.manager.admin_view.start()

        else:
            self.invalid_option()

    def handle_client_options(self, option):

        if option == 1:
            self.list_movies_in_playing()

        elif option == 2:
            self.show_my_tickets()
            self.start()

        elif option == 3:
            self.process_purchase()

        elif option == 4:
            self.logout()
            self.manager.home_view.start()
            return False

        elif option == 5:
            if self.close():
                return False
            else:
                return True
        else:
            self.invalid_option()
        return True
