from time import sleep
from typing import Optional
from pydantic import ValidationError
from src.views.base_view import BaseView


class AuthView(BaseView):
    def __init__(self, manager):
        super().__init__()
        self.manager = manager

    def login(self) -> Optional[str]:
        token = self.token.load_token()
        if token:
            user_role = self.token.get_role_from_token(token)
            if user_role:
                return user_role

        while True:
            self.terminal.clear()
            self.printer.generic('Bem-vindo á Pycine!', line=True)
            person_data: dict = self.inputs.input_login()
            try:
                person = self.person_crud.select_by_credentials(person_data)
                if person:
                    person_id: str = person[0]
                    person_role: str = self.person_crud.get_person_role(
                        person_id)

                    token = self.token.create_token_map(person_id)
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

    def register(self) -> None:
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

            except Exception as e:
                self.terminal.clear()
                self.printer.error(f'Erro ao registrar-se: {str(e)}')

            else:
                self.terminal.clear()
                self.printer.success('Registro realizado com sucesso!')
                self.manager.start()
                break
