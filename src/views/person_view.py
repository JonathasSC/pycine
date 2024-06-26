from src.views.base_view import BaseView


class PersonView(BaseView):
    def __init__(self):
        super().__init__()

        self.list_options: list = [
            'Gerenciar Admins',
            'Gerenciar Persons',
            'Gerenciar Clients',
            'Sair'
        ]

        self.option_actions = {
            1: self.manage_admin,
            3: self.exit
        }

    def start(self):
        try:
            self.terminal.clear()
            self.printer.generic('Escolha uma opção', line=True)
            option: int = self.choose_an_option(self.list_options)
            self.execute_option(self.option_actions, option)
        except Exception as e:
            self.printer.error(e)

    def manage_admin(self):
        while True:
            def add_admin():
                try:
                    self.terminal.clear()
                    self.printer.generic(
                        'Coloque as credenciais do novo admin', line=True)
                    self.create_admin()
                except Exception as e:
                    self.printer.error(e)

            manage_options: list = [
                'Adicionar admin',
                'Sair'
            ]

            manage_actions = {
                1: add_admin,
                2: self.exit,
            }

            try:
                self.terminal.clear()
                self.printer.generic('Escolha uma opção', line=True)
                option: int = self.choose_an_option(manage_options)
                self.execute_option(manage_actions, option)

            except Exception as e:
                self.printer.error(e)
