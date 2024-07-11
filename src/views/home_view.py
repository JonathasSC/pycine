from src.views.base_view import BaseView
from src.views.auth_view import AuthView
from src.views.admin_view import AdminView
from src.crud.admins_crud import AdminsCrud
from src.views.client_view import ClientView

from src.utils.token import Token


class HomeView(BaseView):
    def __init__(self):
        super().__init__()

        self.token_manager: Token = Token()
        self.auth_view: AuthView = AuthView()
        self.admin_view: AdminView = AdminView()
        self.client_view: ClientView = ClientView()
        self.admins_crud: AdminsCrud = AdminsCrud()

        self.list_options: list = [
            'Login',
            'Register',
            'Sair'
        ]

        self.option_actions = {
            1: self.redirect_before_login,
            2: self.auth_view.register,
            3: self.exit
        }

    def start(self):
        while True:
            try:
                if self.admins_crud.get_count_admin() == 0:
                    self.terminal.clear()
                    self.printer.generic('Create first admin', line=True)
                    self.create_admin()

                token = self.token.load_token()
                if token:
                    person_role = self.token.get_role_from_token(token)
                    if person_role:
                        self.redirect_to_role(person_role)
                        return

                self.terminal.clear()
                option: int = self.choose_an_option(
                    options=self.list_options,
                    text='Pycine - Your cinema in terminal'
                )

                self.execute_option(self.option_actions, option)
                break

            except Exception as e:
                self.printer.error(f'Erro ao iniciar Inicial {e}')

    def redirect_before_login(self):
        person_role: str = self.auth_view.login()
        self.redirect_to_role(person_role)
        self.start()

    def redirect_to_role(self, person_role: str):
        if person_role == 'client':
            self.client_view.start()
        elif person_role == 'admin':
            self.admin_view.start()

    def exit(self):
        self.terminal.clear()
        self.printer.generic('Você saiu com sucesso!', line=True, timer=True)
        self.terminal.clear()
