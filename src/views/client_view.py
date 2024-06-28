from src.views.base_view import BaseView
from src.crud.movies_crud import MoviesCrud
from src.crud.sessions_crud import SessionsCrud
from time import sleep


class ClientView(BaseView):
    def __init__(self):
        super().__init__()

        self.movies_crud: MoviesCrud = MoviesCrud()
        self.session_crud: SessionsCrud = SessionsCrud()

        self.list_options: list = [
            'Ver filmes em exibição',
            'Comprar ingresso',
            'Sair'
        ]

        self.option_actions = {
            1: self.list_movies,
            2: self.buy_ticket,
            3: self.exit
        }

    def start(self):
        while True:
            try:
                self.terminal.clear()
                option: int = self.choose_an_option(self.list_options)
                self.execute_option(self.option_actions, option)
                break

            except Exception as e:
                self.printer.error(f'Erro ao iniciar tela publica: {e}')

    def buy_ticket(self):
        while True:
            try:
                movies: list = self.movies_crud.select_all_movies()

                movies_names = [movie[1] for movie in movies]
                movies_id = [movie[0] for movie in movies]

                option: int = self.choose_an_option(movies_names)

                chosen_movie_id: str = movies_id[option]
                chosen_movie_name: str = movies_id[option]

                valid_sessions: list = self.session_crud.select_session_by_movie_id(
                    chosen_movie_id
                )

                print(valid_sessions)
                sleep(5)
                break

            except Exception as e:
                self.printer.error(e)

    def list_movies(self):
        while True:
            self.terminal.clear()
            self.printer.generic(text='Filmes em cartaz', line=True)
            try:
                movies_list: list = self.movies_crud.select_all_movies()
                headers: list = ['NAME', 'GENRE', 'TIME', 'SYNOPSIS']
                movies_compacted: list = [[
                    movie[1],
                    movie[2],
                    movie[3],
                    movie[4]
                ] for movie in movies_list]

                self.printer.display_table(headers, movies_compacted)
                input('Voltar? [press enter]')
                break

            except Exception as e:
                print(f'Erro ao mostrar filmes {e}')
