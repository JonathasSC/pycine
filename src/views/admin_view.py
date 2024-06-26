from src.views.base_view import BaseView
from src.crud.movies_crud import MoviesCrud
from src.crud.admins_crud import AdminsCrud
from src.crud.persons_crud import PersonsCrud

from src.views.movie_view import MovieView
from src.views.room_view import RoomView


class AdminView(BaseView):
    def __init__(self):
        super().__init__()

        self.movies_crud: MoviesCrud = MoviesCrud()
        self.admins_crud: AdminsCrud = AdminsCrud()
        self.person_crud: PersonsCrud = PersonsCrud()

        self.movie_view: MovieView = MovieView()
        self.room_view: RoomView = RoomView()

        self.list_options: list = [
            'Adicionar novo admin',
            'Gerenciar filmes',
            'Gerenciar salas',
            'Sair'
        ]

        self.option_actions = {
            1: self.create_new_admin,
            2: self.movie_view.start,
            3: self.room_view.start,
            4: self.exit
        }

    def start(self):
        try:
            self.terminal.clear()
            self.printer.generic('Choice a option', line=True)
            option: int = self.choose_an_option(self.list_options)
            self.execute_option(self.option_actions, option)
        except Exception as e:
            self.printer.error(e)

    def create_new_admin(self):
        try:
            self.terminal.clear()
            self.printer.generic('Enter new admin credentials', line=True)
            self.create_admin()
        except Exception as e:
            self.printer.error(e)
