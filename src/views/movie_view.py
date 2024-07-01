from src.views.base_view import BaseView
from src.crud.movies_crud import MoviesCrud


class MovieView(BaseView):
    def __init__(self):
        super().__init__()
        self.movies_crud: MoviesCrud = MoviesCrud()
        self.before_view = None

        self.list_options: list = [
            'Adicionar novo filme',
            'Ver lista de filmes',
            'Voltar',
        ]

        self.option_actions = {
            1: self.create_movie,
            2: self.list_movies,
            3: self.back_to_admin
        }

    def set_before_view(self, view):
        self.before_view = view

    def back_to_admin(self):
        if self.before_view:
            self.before_view.start()
        self.printer.error('AdminView não definida')

    def start(self):
        while True:
            try:
                self.terminal.clear()
                self.printer.generic('Choice a option', line=True)
                option: int = self.choose_an_option(self.list_options)
                self.execute_option(self.option_actions, option)
                break

            except Exception as e:
                self.printer.error(f'Erro ao iniciar movie view {e}')
                self.exit()

    def create_movie(self):
        while True:
            try:
                self.terminal.clear()
                self.printer.generic('Enter new movie fields', line=True)
                movie_data: dict = self.inputs.input_movie()
                self.movies_crud.insert_movie(movie_data)
                self.printer.success('Filme adicionado com sucesso!')
                self.start()

            except Exception as e:
                self.printer.error(f'Erro ao criar filme: {e}')
                self.start()

    def list_movies(self):
        while True:
            try:
                self.terminal.clear()
                header = ['ID', 'NAME', 'GENRE', 'DURATION', 'SYNOPSIS']
                movies_list: list = self.movies_crud.select_all_movies()
                movies_formated: list = [[
                    movie[0],
                    movie[1],
                    movie[2],
                    movie[3],
                    f'{str(movie[4])[:50]}...'
                ] for movie in movies_list]

                self.printer.display_table(header, movies_formated)
                input('Voltar? [press enter]')
                self.start()

            except Exception as e:
                self.printer.error(f'Erro ao mostrar filmes: {e}')
                self.start()
