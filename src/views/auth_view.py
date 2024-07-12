from time import sleep
from typing import Optional
from pydantic import ValidationError

from src.utils.uuid import UUID
from src.utils.token import Token
from src.utils.printer import Printer
from src.utils.terminal import Terminal
from src.utils.exceptions import ExceptionsHandlers

from src.crud.admins_crud import AdminsCrud
from src.crud.persons_crud import PersonsCrud
from src.crud.clients_crud import ClientsCrud
from src.views.base_view import BaseView
from src.views.admin_view import AdminView
from src.views.client_view import ClientView


class AuthView(BaseView):
    def __init__(self, manager):
        super().__init__()

        self.manager = manager

        self.admins_crud: AdminsCrud = AdminsCrud()
        self.clients_crud: ClientsCrud = ClientsCrud()
        self.persons_crud: PersonsCrud = PersonsCrud()

        self.uuid: UUID = UUID()
        self.printer: Printer = Printer()
        self.token_manager: Token = Token()
        self.terminal: Terminal = Terminal()

        self.admin_view: AdminView = AdminView(self.manager)
        self.client_view: ClientView = ClientView(self.manager)

        self.handlers: ExceptionsHandlers = ExceptionsHandlers()

        self.list_options: list = ['Login', 'Register', 'Sair']

    def start(self):
        while True:
            try:
                if self.admins_crud.get_count_admin() == 0:
                    self.terminal.clear()
                    self.printer.generic('Crie o primeiro admin:', line=True)
                    self.create_admin()

                self.terminal.clear()
                self.printer.generic('Pycine: cinema pelo terminal', line=True)
                option: int = self.choose_an_option(self.list_options)

                match option:
                    case 1:
                        self.login()
                    case 2:
                        self.register()
                    case 3:
                        self.exit()
                        return
                    case _:
                        self.invalid_option()
                        self.start()

            except Exception as e:
                self.printer.error(
                    f'Erro ao iniciar tela de autenticação: {e}')

    def login(self):
        token = self.token_manager.load_token()
        if token:
            user_role = self.token.get_role_from_token(token)
            if user_role:
                return user_role

        while True:
            self.terminal.clear()
            self.printer.generic('Bem-vindo á Pycine!', line=True)
            person_data: dict = self.inputs.input_login()
            try:
                person = self.persons_crud.select_by_credentials(person_data)
                if person:
                    person_id: str = person[0]
                    person_role: str = self.persons_crud.get_person_role(
                        person_id)

                    token = self.token_manager.create_token_map(person_id)
                    self.terminal.clear()
                    self.printer.success('Login realizado com sucesso')
                    return person_role

                else:
                    self.terminal.clear()
                    self.printer.error(
                        'Credenciais erradas, tente novamente...')

            except ValidationError as e:
                self.terminal.clear()
                self.handlers.handle_validation_error(e)

            except Exception as e:
                self.terminal.clear()
                self.printer.error(f'Erro ao fazer login: {e}')

    def register(self):
        while True:
            self.terminal.clear()
            self.printer.generic('Crie sua conta agora!', line=True)
            person_data: dict = {}

            try:
                person_data: dict = self.inputs.input_register()
                self.persons_crud.insert_person(person_data)
                person_created: tuple = self.persons_crud.select_by_email(
                    person_data['email'])
                self.clients_crud.insert_client(person_created[0])

            except ValidationError as e:
                self.terminal.clear()

                for erro in e.errors():
                    self.printer.error(
                        text=erro['msg'][12:],
                        line=False,
                        timer=False
                    )

                    self.printer.line(len(erro['msg'][12:]), color='red')
                sleep(5)

            except Exception as e:
                self.terminal.clear()
                self.printer.error(f'Erro ao registrar-se: {str(e)}')

            else:
                self.terminal.clear()
                self.printer.success('Registro realizado com sucesso!')
                self.start()
                break
