from typing import Optional
from pydantic import ValidationError

from src.utils.uuid import UUID
from src.utils.printer import Printer
from src.utils.exceptions import ExceptionsHandlers
from src.utils.terminal import Terminal

from src.crud.persons_crud import PersonsCrud
from src.crud.clients_crud import ClientsCrud
from src.crud.admins_crud import AdminsCrud

from src.views.base_view import BaseView
from src.views.admin_view import AdminView
from src.views.client_view import ClientView
from src.utils.token import Token

from time import sleep


class AuthView(BaseView):
    def __init__(self):
        super().__init__()
        self.uuid: UUID = UUID()
        self.clients_crud: ClientsCrud = ClientsCrud()
        self.persons_crud: PersonsCrud = PersonsCrud()
        self.admins_crud: AdminsCrud = AdminsCrud()
        self.printer: Printer = Printer()
        self.terminal: Terminal = Terminal()
        self.handlers: ExceptionsHandlers = ExceptionsHandlers()
        self.admin_view: AdminView = AdminView()
        self.client_view: ClientView = ClientView()
        self.token_manager: Token = Token()

        self.list_options: list = ['Login', 'Register', 'Sair']
        self.option_actions = {1: self.login, 2: self.register, 3: self.exit}

    def start(self):
        if self.admins_crud.get_count_admin() == 0:
            self.terminal.clear()
            self.printer.generic('Crie o primeiro admin:', line=True)
            self.create_admin()

        self.terminal.clear()
        self.printer.generic('Pycine - seu cinema pelo terminal', line=True)
        option: int = self.choose_an_option(self.list_options)
        self.execute_option(self.option_actions, option)

    def login(self):
        self.terminal.clear()
        self.printer.generic('Bem-vindo á Pycine!', line=True)

        token = self.token_manager.load_token()
        if token:
            user_role = self.get_role_from_token(token)
            if user_role:
                return user_role

        while True:
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
                    continue
            except ValidationError as e:
                self.handlers.handle_validation_error(e)
            except Exception as e:
                self.printer.error(f'Erro ao fazer login: {e}')

    def register(self):
        self.terminal.clear()
        self.printer.generic('Crie sua conta agora!', line=True)
        person_data: dict = {}
        while True:
            try:
                person_data: dict = self.inputs.input_person()
                self.persons_crud.insert_person(person_data)
                person_created: tuple = self.persons_crud.select_by_email(
                    person_data['email'])
                self.clients_crud.insert_client(person_created[0])
            except ValidationError as e:
                self.handlers.handle_validation_error(e)
            except Exception as e:
                self.printer.error(f'Erro ao registrar-se: {str(e)}')
            else:
                self.printer.success('Registro realizado com sucesso!')
                break

    def get_role_from_token(self, token: str) -> Optional[str]:
        user_id = self.token_manager.person_role_from_token(token)
        if user_id:
            return self.persons_crud.get_person_role(user_id)
        return None

    def exit(self):
        self.token_manager.delete_token()
        self.printer.generic('Você saiu com sucesso!', line=True)
        self.terminal.clear()
