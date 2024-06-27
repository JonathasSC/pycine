from src.views.base_view import BaseView
from src.crud.movies_crud import MoviesCrud
from src.crud.admins_crud import AdminsCrud
from src.crud.persons_crud import PersonsCrud

from src.views.person_view import PersonView
from src.views.client_view import ClientView
from src.views.movie_view import MovieView
from src.views.room_view import RoomView


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

        self.list_options: list = [
            'Fluxo publico',
            'Fluxo administrativo',
            'Logout',
            'Sair',
        ]

    def start(self):
        while True:
            try:
                self.terminal.clear()
                option: int = self.choose_an_option(self.list_options)
                match option:
                    case 1:
                        self.public_flow()
                    case 2:
                        self.admin_flow()
                    case 3:
                        self.logout()
                        return
                    case 4:
                        self.exit()
                        return

            except Exception as e:
                self.printer.error(f'Erro ao iniciar tela de admin: {e}')

    def public_flow(self):
        client_view = ClientView()
        client_view.start()

    def admin_flow(self):
        self.room_view.set_before_view(self)

        admin_options: list = [
            'Gerenciar pessoas',
            'Gerenciar filmes',
            'Gerenciar salas',
            'Voltar',
            'Sair'
        ]

        admin_actions = {
            1: self.person_view.start,
            2: self.movie_view.start,
            3: self.room_view.start,
            4: self.start,
            5: self.exit
        }

        try:
            self.terminal.clear()
            option: int = self.choose_an_option(admin_options)
            self.execute_option(admin_actions, option)

        except Exception as e:
            self.printer.error(e)
