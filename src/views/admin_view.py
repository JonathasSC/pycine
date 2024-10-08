from src.views.base_view import BaseView
from src.utils.inputs import Inputs


class AdminView(BaseView):
    def __init__(self, manager):
        super().__init__()
        self.manager = manager
        self.inputs = Inputs()

        self.list_options: list = [
            'Fluxo publico',
            'Fluxo administrativo',
            'Sair da conta',
            'Fechar',
        ]

    def start(self) -> None:
        self.logger.info('FLUXO DE ADMINISTRADOR')

        while True:
            try:
                self.terminal.clear()
                option: int = self.inputs.input_an_option(
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
                        if self.close(text='Realmente deseja sair?'):
                            self.printer.generic(
                                text='Saindo...',
                                line=True,
                                timer=True,
                                clear=True
                            )
                            self.logout()
                        self.manager.home_view.start()
                    case 4:
                        if self.close():
                            self.terminal.clear()
                            break
                        self.manager.admin_view.start()
                    case _:
                        self.invalid_option()
                        self.start()
                break

            except Exception as e:
                self.printer.error(f'Erro ao iniciar tela de admin: {e}')

    def admin_flow(self) -> None:
        self.logger.info('OPÇÕES DE ADMINISTRADOR')

        admin_options: list = [
            'Gerenciar pessoas',
            'Gerenciar filmes',
            'Gerenciar salas',
            'Gerenciar sessões',
            'Gerenciar cadeiras',
            'Gerenciar tickets',
            'Voltar',
        ]

        try:
            self.terminal.clear()
            option: int = self.inputs.input_an_option(admin_options)
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
                    self.manager.seat_view.start()
                case 6:
                    self.manager.ticket_view.start()
                case 7:
                    self.manager.admin_view.start()
                case _:
                    self.invalid_option()
                    self.start()

        except Exception as e:
            self.printer.error(e)
