from pydantic import ValidationError

from src.views.base_view import BaseView
from src.crud.movies_crud import MoviesCrud
from src.crud.admins_crud import AdminsCrud
from src.crud.persons_crud import PersonsCrud

from tabulate import tabulate


class AdminView(BaseView):
    def __init__(self):
        super().__init__()

        self.movies_crud: MoviesCrud = MoviesCrud()
        self.admins_crud: AdminsCrud = AdminsCrud()
        self.person_crud: PersonsCrud = PersonsCrud()

        self.list_options: list = [
            'Adicionar novo admin',
            'Adicionar novo filme',
            'Visualizar filmes',
            'Sair'
        ]

        self.option_actions = {
            1: self.create_new_admin,
            2: self.create_new_movie,
            3: self.view_movies,
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

    def create_new_movie(self):
        try:
            self.terminal.clear()
            self.printer.generic('Enter new movie fields', line=True)
            movie_data: dict = self.inputs.input_movie()
            self.movies_crud.insert_movie(movie_data)
        except Exception as e:
            self.printer.error(e)

    def view_movies(self):
        try:
            self.terminal.clear()
            header = ['ID', 'NAME', 'DURATION', 'SYNOPSIS']
            movies_list: list = self.movies_crud.select_all_movies()
            self.printer.display_table(header, movies_list)
        except Exception as e:
            print(f'Erro ao mostrar filmes {e}')
