import click
from src.utils.printer import Printer
from src.schemas.person_schemas import PersonCreate
from src.crud.persons_crud import PersonsCrud
from src.utils.uuid import UUID
from pydantic import ValidationError
from src.utils.exceptions import ExceptionsHandlers


class AuthView:
    def __init__(self):
        self.printer: Printer = Printer()
        self.handlers: ExceptionsHandlers = ExceptionsHandlers()

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

        self.uuid: UUID = UUID()
        self.persons_crud = PersonsCrud()

    def start(self):
        self.printer.generic('Pycine - Your cinema in terminal', line=True)
        option: int = self.choose_an_option()
        self.execute_option(option)

    def choose_an_option(self):
        while True:
            try:
                self.printer.option_list(self.list_options)
                option: int = int(input('Digite uma opção: '))

                if option not in range(1, len(self.list_options)):
                    self.printer.error('Opção inexistente, tente novamente')
                    continue
                return option

            except ValueError:
                self.printer.error('Valor inválido, tente novamente')

    def execute_option(self, option: int):
        action = self.option_actions.get(option, self.invalid_option)
        action()

    def login(self):
        self.printer.generic('Login process started', line=True)
        pass

    def register(self):
        self.printer.generic('Create your account now!', line=True)

        while True:
            name = input('Nome: ')
            email = input('Email: ')
            password = input('Senha: ')

            person_data = {
                "name": name,
                "email": email,
                "password": password,
            }

            try:
                PersonCreate(**person_data)
                self.persons_crud.insert_person(person_data)
                self.printer.success('Registro realizado com sucesso!')
                return True

            except ValidationError as e:
                self.handlers.handle_validation_error(e)
            except Exception as e:
                self.printer.error(f'Register error: {str(e)}')

    def exit(self):
        self.printer.generic('Saindo...', line=True)

    def invalid_option(self):
        self.printer.error('Opção inválida, tente novamente')


if __name__ == "__main__":
    flow = AuthView()
    flow.start()
