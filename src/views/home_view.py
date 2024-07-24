from src.views.base_view import BaseView


class HomeView(BaseView):
    def __init__(self, manager):
        super().__init__()
        self.manager = manager

        self.list_options: list = [
            'Login',
            'Register',
            'Sair'
        ]

    def start(self):
        while True:
            try:
                if self.admin_crud.get_count_admin() == 0:
                    self.terminal.clear()
                    self.printer.generic('Create first admin', line=True)
                    self.create_admin()

                token = self.token.load_token()
                person_role = self.token.get_role_from_token(token)

                if token and person_role:
                    if person_role == 'client':
                        self.manager.client_view.start()
                        break

                    elif person_role == 'admin':
                        self.manager.admin_view.start()
                        break

                self.terminal.clear()

                option: int = self.choose_an_option(
                    options=self.list_options,
                    text='Pycine - Your cinema in terminal'
                )

                if option == 1:
                    self.manager.auth_view.login()
                    self.start()

                elif option == 2:
                    self.manager.auth_view.register()
                    self.manager.auth_view.login()
                    self.start()

                elif option == 3:
                    self.close()
                    break
                break

            except Exception as e:
                self.printer.error(f'Erro ao iniciar Inicial {e}')
