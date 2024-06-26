from src.views.base_view import BaseView
from src.crud.movies_crud import MoviesCrud


class MovieView(BaseView):
    def __init__(self):
        super().__init__()
        self.movies_crud: MoviesCrud = MoviesCrud()

        self.list_options: list = [
            'Adicionar novo filme',
            'Ver lista de filmes',
            'Sair'
        ]

        self.option_actions = {
            1: self.create_movie,
            2: self.list_movies,
            3: self.exit
        }

    def start(self):
        try:
            self.terminal.clear()
            self.printer.generic('Choice a option', line=True)
            option: int = self.choose_an_option(self.list_options)
            self.execute_option(self.option_actions, option)
        except Exception as e:
            self.printer.error(e)

    def create_movie(self):
        try:
            self.terminal.clear()
            self.printer.generic('Enter new movie fields', line=True)
            movie_data: dict = self.inputs.input_movie()
            self.movies_crud.insert_movie(movie_data)

            self.printer.success(
                text='Filme adicionado com sucesso!',
                line=True,
                timer=True
            )

        except Exception as e:
            self.printer.error(e)

    def list_movies(self):
        try:
            self.terminal.clear()
            header = ['ID', 'NAME', 'DURATION', 'SYNOPSIS']
            movies_list: list = self.movies_crud.select_all_movies()
            self.printer.display_table(header, movies_list)
        except Exception as e:
            print(f'Erro ao mostrar filmes {e}')