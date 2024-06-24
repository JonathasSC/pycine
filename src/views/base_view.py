from src.utils.printer import Printer
from src.utils.exceptions import ExceptionsHandlers
from src.utils.terminal import Terminal


class BaseView:
    def __init__(self):
        self.printer: Printer = Printer()
        self.terminal: Terminal = Terminal()
        self.handlers: ExceptionsHandlers = ExceptionsHandlers()

    def start(self):
        raise NotImplementedError(
            "Subclasses should implement start() method.")

    def choose_an_option(self, options: list):
        while True:
            try:
                self.printer.option_list(options)
                option: int = int(input('Digite uma opção: '))

                if option not in range(1, len(options) + 1):
                    self.printer.error('Opção inválida, tente novamente')
                    continue

                return option

            except ValueError:
                self.printer.error('Valor inválido, tente novamente')

    def execute_option(self, options: dict, option: int):
        action = options.get(option, self.invalid_option)
        action()

    def invalid_option(self):
        self.terminal.clear()
        self.printer.error('Opção inválida, tente novamente')

    def exit(self):
        self.printer.generic('Saindo...', line=True)
