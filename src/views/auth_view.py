from pydantic import ValidationError

from src.utils.uuid import UUID
from src.utils.printer import Printer
from src.utils.exceptions import ExceptionsHandlers
from src.utils.terminal import Terminal

from src.crud.persons_crud import PersonsCrud
from src.crud.clients_crud import ClientsCrud
from src.views.base_view import BaseView
from src.views.admin_view import AdminView
from src.views.client_view import ClientView


class AuthView(BaseView):
    def __init__(self):
        super().__init__()

        self.uuid: UUID = UUID()
        self.client_crud: ClientsCrud = ClientsCrud()
        self.persons_crud: PersonsCrud = PersonsCrud()

        self.printer: Printer = Printer()
        self.terminal: Terminal = Terminal()
        self.handlers: ExceptionsHandlers = ExceptionsHandlers()
        self.admin_view: AdminView = AdminView()
        self.client_view: ClientView = ClientView()

        self.list_options: list = [
            'Login',
            'Register',
            'Sair'
        ]

        self.option_actions = {
            1: self.login,
            2: self.register,
            3: self.exit
        }

    def start(self):
        self.printer.generic('Pycine - Your cinema in terminal', line=True)
        option: int = self.choose_an_option(self.list_options)
        self.execute_option(self.option_actions, option)

    def login(self):
        self.terminal.clear()
        self.printer.generic('Welcome to the pycine!', line=True)
        person_data: dict = {}

        while True:
            person_data['email'] = input('Email: ')
            person_data['password'] = input('Senha: ')

            try:
                person: bool = self.persons_crud.select_by_credentials(
                    person_data)

                if person:
                    person_id: str = person[0]
                    person_role: str = self.persons_crud.get_person_role(
                        person_id)

                    if person_role == 'admin':
                        self.printer.success('Login realizado como admin')
                        admin_view = AdminView()
                        admin_view.start()
                        return
                    elif person_role == 'client':
                        self.printer.success('Login realizado como cliente')
                        client_view = ClientView()
                        client_view.start()
                        return
                    else:
                        self.printer.error('Função de usuário desconhecida')
                        continue
                else:
                    self.printer.error('Credenciais inválidas.')

            except ValidationError as e:
                self.handlers.handle_validation_error(e)
            except Exception as e:
                self.printer.error(f'Credenciais erradas, tente novamente...')

    def register(self):
        self.terminal.clear()
        self.printer.generic('Create your account now!', line=True)
        person_data: dict = {}

        while True:
            person_data['name'] = input('Nome: ')
            person_data['email'] = input('Email: ')
            person_data['password'] = input('Senha: ')

            try:
                self.persons_crud.insert_person(person_data)
                person_created: tuple = self.persons_crud.select_by_email(
                    person_data['email']
                )
                self.client_crud.insert_client(person_created[0])
            except ValidationError as e:
                self.handlers.handle_validation_error(e)
            except Exception as e:
                self.printer.error(f'Register error: {str(e)}')
            else:
                self.printer.success('Registro realizado com sucesso!')


if __name__ == "__main__":
    flow = AuthView()
    flow.start()
