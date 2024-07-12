from src.views.base_view import BaseView
from src.crud.movies_crud import MoviesCrud
from src.crud.admins_crud import AdminsCrud
from src.crud.persons_crud import PersonsCrud

# from src.views.home_view import HomeView
from src.views.room_view import RoomView
from src.views.movie_view import MovieView
from src.views.person_view import PersonView
from src.views.client_view import ClientView
from src.views.session_view import SessionView


class AdminView(BaseView):
    def __init__(self, manager):
        super().__init__()

        self.manager = manager
        self.back_view = None

        self.movies_crud: MoviesCrud = MoviesCrud()
        self.admins_crud: AdminsCrud = AdminsCrud()
        self.person_crud: PersonsCrud = PersonsCrud()

        self.room_view: RoomView = RoomView(self.manager)
        self.movie_view: MovieView = MovieView(self.manager)
        self.client_view: ClientView = ClientView(self.manager)
        self.person_view: PersonView = PersonView(self.manager)
        self.session_view: SessionView = SessionView(self.manager)

        self.list_options: list = [
            'Fluxo publico',
            'Fluxo administrativo',
            'Logout',
            'Sair',
        ]

    def start(self):
        self.logger.info('START ADMIN VIEW')
        while True:
            try:
                self.terminal.clear()
                option: int = self.choose_an_option(
                    self.list_options, text='Escolha o que gerenciar')

                if option == 1:
                    self.manager.client_view.start(True)

                elif option == 2:
                    self.admin_flow()

                elif option == 3:
                    self.logout()
                    self.manager.home_view.start()

                elif option == 4:
                    self.close()
                    break

                else:
                    self.invalid_option()
                    continue

                break
            except Exception as e:
                self.printer.error(f'Erro ao iniciar tela de admin: {e}')

    def admin_flow(self):
        self.logger.info('START ADMIN FLOW')

        admin_options: list = [
            'Gerenciar pessoas',
            'Gerenciar filmes',
            'Gerenciar salas',
            'Gerenciar sessões',
            'Voltar',
        ]

        admin_actions = {
            1: self.person_view.start,
            2: self.movie_view.start,
            3: self.room_view.start,
            4: self.session_view.start,
            5: self.start
        }

        try:
            self.terminal.clear()
            option: int = self.choose_an_option(admin_options)
            if option in admin_actions:
                admin_actions[option]()
            else:
                self.invalid_option()

        except Exception as e:
            self.printer.error(e)

    def confirm_close(self):
        self.terminal.clear()

        confirm_options = ['Sim', 'Não']
        option = self.choose_an_option(
            confirm_options, text='Realmente deseja sair?')

        if option == 1:
            self.terminal.clear()
            self.printer.generic('Fechado...', line=True, timer=True)
            self.terminal.clear()
            return True

        return False

    def close(self):
        if self.confirm_close():
            return True
        return False
