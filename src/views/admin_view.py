from src.views.base_view import BaseView


class AdminView(BaseView):
    def __init__(self, manager):
        super().__init__()
        self.manager = manager

        self.list_options: list = [
            'Fluxo publico',
            'Fluxo administrativo',
            'Logout',
            'Sair',
        ]

    def start(self) -> None:
        while True:
            try:
                self.terminal.clear()
                option: int = self.choose_an_option(
                    self.list_options,
                    text='Escolha o que gerenciar')

                match option:
                    case 1:
                        self.terminal.clear()
                        self.manager.client_view.start()
                        break
                    case 2:
                        self.terminal.clear()
                        self.manager.admin_view.admin_flow()
                        break
                    case 3:
                        self.logout()
                        self.manager.home_view.start()
                    case 4:
                        if self.close():
                            break
                    case _:
                        self.invalid_option()
                        self.start()

            except Exception as e:
                self.printer.error(f'Erro ao iniciar tela de admin: {e}')

    def admin_flow(self) -> None:
        self.logger.info('START ADMIN FLOW')

        admin_options: list = [
            'Gerenciar pessoas',
            'Gerenciar filmes',
            'Gerenciar salas',
            'Gerenciar sessões',
            'Voltar',
        ]

        try:
            self.terminal.clear()
            option: int = self.choose_an_option(admin_options)
            match option:
                case 1:
                    self.manager.person_view.start()
                case 2:
                    self.manager.movie_view.start()
                case 3:
                    self.manager.room_view.start()
                case 4:
                    self.manager.session_view.start()
                case 5:
                    self.manager.admin_view.start()
                case _:
                    self.invalid_option()
                    self.start()

        except Exception as e:
            self.printer.error(e)
