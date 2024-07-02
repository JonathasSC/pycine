from src.views.base_view import BaseView
from src.crud.movies_crud import MoviesCrud
from src.crud.sessions_crud import SessionsCrud
from src.crud.rooms_crud import RoomsCrud
import traceback
from time import sleep


class ClientView(BaseView):
    def __init__(self):
        super().__init__()

        self.room_crud: RoomsCrud = RoomsCrud()
        self.movies_crud: MoviesCrud = MoviesCrud()
        self.session_crud: SessionsCrud = SessionsCrud()

        self.list_options: list = [
            'Ver filmes em exibição',
            'Comprar ingresso',
            'Sair'
        ]

        self.option_actions = {
            1: self.list_movies_in_playing,
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
                traceback.print_exc()
                sleep(10)
                self.printer.error(f'Erro ao iniciar tela publica: {e}')

    def buy_ticket(self):
        while True:
            try:
                sessions: list = self.session_crud.select_all_session_with_movies()

                if not sessions:
                    self.terminal.clear()
                    self.printer.warning("Nenhum filme disponível.")
                    self.start()

                movies_names = [session[0] for session in sessions]
                movies_names = [session[0] for session in sessions]
                movies_id = [session[4] for session in sessions]

                self.terminal.clear()
                movie_option: int = self.choose_an_option(
                    options=movies_names,
                    cancel=True
                )

                if movie_option is None:
                    self.start()

                chosen_movie_id: str = movies_id[movie_option - 1]

                self.terminal.clear()
                sessions: list = self.session_crud.select_sessions_with_room_details(
                    chosen_movie_id
                )

                if not sessions:
                    self.terminal.clear()
                    self.printer.warning("Nenhuma sessão disponível.")
                    self.start()

                sessions_formated: list = [
                    f'{session[2].center(10, " ")} | {session[1].center(10, " ")} | {session[3].center(10, " ")} | {session[0].center(10, " ")}'
                    for session in sessions
                ]

                session_option: int = self.choose_an_option(
                    sessions_formated,
                    'Escolha uma sessão',
                    True
                )

                if session_option is None:
                    self.start()

                input('Voltar? [press enter]')
                self.start()
                break

            except IndexError as e:
                print("Erro ao acessar a lista de filmes ou sessões.")
                traceback.print_exc()

            except Exception as e:
                self.printer.error(e)
                traceback.print_exc()

    def list_movies_in_playing(self):
        while True:
            try:
                movies_list: list = self.session_crud.select_all_session_with_movies()

                if not movies_list:
                    self.terminal.clear()
                    self.printer.warning("Nenhum filme com sessão disponivel.")
                    self.start()

                self.terminal.clear()
                self.printer.generic(text='Filmes em cartaz', line=True)
                headers: list = ['NAME', 'GENRE', 'DURATION', 'SYNOPSIS']

                movies_compacted: list = [[
                    movie[0],
                    movie[1],
                    movie[2],
                    f'{str(movie[3])[:50]}...'
                ] for movie in movies_list]

                self.printer.display_table(headers, movies_compacted)
                input('Voltar? [press enter]')
                break

            except Exception as e:
                print(f'Erro ao mostrar filmes {e}')
