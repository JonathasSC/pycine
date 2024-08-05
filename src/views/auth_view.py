from typing import Optional
from pydantic import ValidationError
from src.views.base_view import BaseView


class AuthView(BaseView):
    def __init__(self, manager):
        super().__init__()
        self.manager = manager
        self.logger.info('FLUXO DE AUTENTICAÇÃO')

    def login(self) -> Optional[str]:
        self.logger.info('AREA DE LOGIN')
        while True:
            try:
                token = self.token.load_token()
                if token:
                    user_role = self.token.get_role_from_token(token)
                    if user_role:
                        return user_role

                self.terminal.clear()
                self.printer.generic(
                    text='Bem-vindo á Pycine!'.center(50)
                )

                self.printer.generic(
                    text='Preencha os campos ou digite "q" para cancelar',
                    line=True)

                person_data: Optional[dict] = self.inputs.input_login()

                if person_data == None:
                    self.printer.warning(
                        text='Login cancelado',
                        clear=True)

                    break

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
                    self.printer.error('Credenciais erradas, tente novamente')

            except ValidationError as e:
                self.terminal.clear()
                self.handlers.handle_validation_error(e)

            except Exception as e:
                self.terminal.clear()
                self.printer.error(f'Erro ao fazer login: {e}')

    def register(self) -> None:
        self.logger.info('AREA DE REGISTRO')

        while True:
            try:
                self.terminal.clear()
                self.printer.generic(
                    text='Crie sua conta agora!'.center(50)
                )

                self.printer.generic(
                    text='Preencha os campos ou digite "q" para cancelar',
                    line=True
                )

                person_data: Optional[dict] = self.inputs.input_register()

                if person_data == None:
                    self.printer.warning(text='Registro cancelado', clear=True)
                    break

                person_id: Optional[str] = self.person_crud.insert_person(
                    person_data)

                self.client_crud.insert_client(person_id)

                self.printer.success(
                    text='Registro efetuado com sucesso!',
                    clear=True)
                break

            except ValidationError as e:
                self.terminal.clear()

                for erro in e.errors():
                    self.printer.error(
                        text=erro['msg'][12:],
                        line=True,
                        timer=True
                    )

                    self.printer.line(len(erro['msg'][12:]), color='red')
                    self.printer.warning(text='Tente novamente', clear=True)

            except ValueError as e:
                self.terminal.clear()
                self.printer.error(f'{e}')

            except Exception as e:
                self.terminal.clear()
                self.printer.error(f'Erro ao registrar-se: {str(e)}')
