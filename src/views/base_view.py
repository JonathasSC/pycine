from pydantic import ValidationError

from src.utils.printer import Printer
from src.utils.exceptions import ExceptionsHandlers
from src.utils.terminal import Terminal
from src.utils.inputs import Inputs
from src.utils.token import Token

from src.utils.logger import Logger
from src.crud.admins_crud import AdminsCrud
from src.crud.persons_crud import PersonsCrud
from src.crud.sessions_crud import SessionsCrud
from src.crud.seats_crud import SeatsCrud
from src.crud.tickets_crud import TicketsCrud


class BaseView:
    def __init__(self):
        self.inputs: Inputs = Inputs()
        self.printer: Printer = Printer()
        self.terminal: Terminal = Terminal()

        self.admin_crud: AdminsCrud = AdminsCrud()
        self.person_crud: PersonsCrud = PersonsCrud()
        self.session_crud: SessionsCrud = SessionsCrud()
        self.ticket_crud: TicketsCrud = TicketsCrud()
        self.seat_crud: SeatsCrud = SeatsCrud()

        self.handlers: ExceptionsHandlers = ExceptionsHandlers()
        self.logger: Logger = Logger()
        self.token: Token = Token()

    def logout(self):
        self.terminal.clear()
        self.printer.generic('Saindo...', line=True, timer=True)
        self.token.delete_token()
        self.terminal.clear()

    def start(self):
        raise NotImplementedError(
            "Subclasses should implement start() method.")

    def choose_an_option(self, options: list, text: str = 'Escolha uma opção', cancel: bool = False):
        while True:
            try:
                self.printer.generic(text, line=True)
                self.printer.option_list(options)

                if cancel:
                    self.printer.generic(f'[0] - Cancelar')
                option: int = int(input('Digite uma opção: '))

                if cancel and option == 0:
                    return None
                if 0 < option <= len(options) + 1:
                    return option
                else:
                    self.terminal.clear()
                    self.printer.error("Opção inválida, Tente novamente.")
                    self.terminal.clear()

            except ValueError:
                self.terminal.clear()
                self.printer.error(
                    "Entrada inválida. Por favor, digite um número.")
                self.terminal.clear()

    def execute_option(self, options: dict, option: int):
        action = options.get(option, self.invalid_option)
        action()

    def invalid_option(self):
        self.terminal.clear()
        self.printer.error('Opção inválida, tente novamente')
        self.terminal.clear()

    def invalid_value(self):
        self.terminal.clear()
        self.printer.error('Valor inválido, tente novamente')
        self.terminal.clear()

    def create_admin(self):
        while True:
            try:
                person_data: dict = self.inputs.input_person()
                self.person_crud.insert_person(person_data)
                person: tuple = self.person_crud.select_by_email(
                    person_data['email'])

                self.admins_crud.insert_admin(person[0])
                self.printer.success('Admin criado com sucesso!')
                break

            except ValidationError as e:
                self.handlers.handle_validation_error(e)
            except Exception as e:
                self.printer.error(f'Erro ao criar admin: {str(e)}')

    def close(self):
        self.terminal.clear()

        confirm_options = ['Sim', 'Não']
        option = self.choose_an_option(
            confirm_options, text='Realmente deseja sair?')

        if option == 1:
            self.terminal.clear()
            self.printer.generic('Fechado...', line=True, timer=True)
            self.terminal.clear()
            return True

        return False
