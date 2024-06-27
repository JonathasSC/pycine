from src.views.base_view import BaseView
from src.views.auth_view import AuthView
from src.views.client_view import ClientView
from src.views.admin_view import AdminView
from src.crud.admins_crud import AdminsCrud
from src.utils.token import Token


class HomeView(BaseView):
    def __init__(self):
        super().__init__()

        self.auth_view: AuthView = AuthView()
        self.client_view: ClientView = ClientView()
        self.admin_view: AdminView = AdminView()
        self.admins_crud: AdminsCrud = AdminsCrud()
        self.token_manager: Token = Token()

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
        if self.admins_crud.get_count_admin() == 0:
            self.terminal.clear()
            self.printer.generic('Create first admin', line=True)
            self.create_admin()

        token = self.token_manager.load_token()
        if token:
            person_role = self.auth_view.get_role_from_token(token)
            if person_role:
                self.redirect_to_role(person_role)
                return

        self.terminal.clear()
        self.printer.generic('Pycine - Your cinema in terminal', line=True)
        option: int = self.choose_an_option(self.list_options)
        self.execute_option(self.option_actions, option)

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
        self.token_manager.delete_token()
        self.printer.generic('Você saiu com sucesso!', line=True)
        self.terminal.clear()
