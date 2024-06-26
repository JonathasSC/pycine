from src.views.base_view import BaseView
from src.crud.movies_crud import MoviesCrud
from src.crud.admins_crud import AdminsCrud
from src.crud.persons_crud import PersonsCrud

from src.views.person_view import PersonView
from src.views.client_view import ClientView
from src.views.movie_view import MovieView
from src.views.room_view import RoomView
from src.views.session_view import SessionView


class AdminView(BaseView):
    def __init__(self):
        super().__init__()

        self.movies_crud: MoviesCrud = MoviesCrud()
        self.admins_crud: AdminsCrud = AdminsCrud()
        self.person_crud: PersonsCrud = PersonsCrud()
        self.person_view: PersonView = PersonView()
        self.client_view: ClientView = ClientView()
        self.movie_view: MovieView = MovieView()
        self.room_view: RoomView = RoomView()
        self.session_view: SessionView = SessionView()

        self.room_view.set_before_view(self)
        self.movie_view.set_before_view(self)
        self.person_view.set_before_view(self)
        self.session_view.set_before_view(self)

        self.list_options: list = [
            'Fluxo publico',
            'Fluxo administrativo',
            'Logout',
            'Sair',
        ]

        self.option_actions = {
            1: self.public_flow,
            2: self.admin_flow,
            3: self.logout,
            4: self.exit
        }

    def start(self):
        while True:
            try:
                self.terminal.clear()
                option: int = self.choose_an_option(
                    self.list_options,
                    text='Escolha o que gerenciar'
                )
                self.execute_option(self.option_actions, option)

            except Exception as e:
                self.printer.error(f'Erro ao iniciar tela de admin: {e}')

    def public_flow(self):
        client_view = ClientView()
        client_view.start()

    def admin_flow(self):

        admin_options: list = [
            'Gerenciar pessoas',
            'Gerenciar filmes',
            'Gerenciar salas',
            'Gerenciar sessões',
            'Voltar',
            'Sair'
        ]

        admin_actions = {

            1: self.person_view.start,
            2: self.movie_view.start,
            3: self.room_view.start,
            4: self.session_view.start,
            5: self.start,
            6: self.exit
        }

        try:
            self.terminal.clear()
            option: int = self.choose_an_option(admin_options)
            self.execute_option(admin_actions, option)

        except Exception as e:
            self.printer.error(e)
