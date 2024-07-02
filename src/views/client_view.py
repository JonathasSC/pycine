from src.views.base_view import BaseView
from src.crud.movies_crud import MoviesCrud
from src.crud.sessions_crud import SessionsCrud

from src.crud.rooms_crud import RoomsCrud
from src.crud.seats_crud import SeatsCrud

import traceback
from time import sleep


class ClientView(BaseView):
    def __init__(self):
        super().__init__()

        self.room_crud: RoomsCrud = RoomsCrud()
        self.movies_crud: MoviesCrud = MoviesCrud()
        self.session_crud: SessionsCrud = SessionsCrud()
        self.seats_crud: SeatsCrud = SeatsCrud()

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
                sessions_with_movies = self.session_crud.select_all_session_with_movies()

                if not sessions_with_movies:
                    self.terminal.clear()
                    self.printer.warning("Nenhum filme disponível.")
                    self.start()

                movie_id = self.choose_movie(sessions_with_movies)
                sessions_with_room_details = self.session_crud.select_sessions_with_room_details(
                    movie_id
                )

                if not sessions_with_room_details:
                    self.terminal.clear()
                    self.printer.warning("Nenhuma sessão disponível.")
                    self.start()

                chosen_session_id = self.choose_session(
                    sessions_with_room_details
                )
                self.printer.generic(chosen_session_id, timer=True)

                session: tuple = self.session_crud.select_session_by_id(
                    chosen_session_id
                )

                self.printer.generic(session, timer=True)
                self.process_ticket_purchase(chosen_session_id)

            except IndexError:
                self.printer.generic(
                    "Erro ao acessar a lista de filmes ou sessões."
                )
                traceback.print_exc()

            except Exception as e:
                self.printer.error(e)
                traceback.print_exc()

    def choose_movie(self, sessions):
        movies_names = [session[0] for session in sessions]
        movies_ids = [session[4] for session in sessions]

        self.terminal.clear()
        movie_option = self.choose_an_option(
            options=movies_names,
            text='Escolha uma sessão',
            cancel=True
        )

        if movie_option is None:
            self.start()

        chosen_movie_id = movies_ids[movie_option - 1]
        return chosen_movie_id

    def choose_session(self, sessions):
        sessions_formatted = [
            f'{session[2].center(10, " ")} | {session[1].center(10, " ")} | {
                session[3].center(10, " ")} | {session[0].center(10, " ")}'
            for session in sessions
        ]

        sessions_ids = [session[5] for session in sessions]

        session_option = self.choose_an_option(
            sessions_formatted,
            'Escolha uma sessão',
            True
        )

        if session_option is None:
            self.start()

        chosen_session_id = sessions_ids[session_option - 1]
        return chosen_session_id

    def process_ticket_purchase(self, chosen_session_id):
        try:
            session = self.session_crud.select_session_by_id(chosen_session_id)

            if not session:
                self.printer.error(
                    f"Sessão com ID {chosen_session_id} não encontrada.")
                return

            room_id = session[3]

            seats = self.seats_crud.get_seats_by_room_id(room_id)

            if not seats:
                self.terminal.clear()
                self.printer.warning(
                    "Nenhuma cadeira disponível para esta sala.")
                input('Voltar? [press enter]')
                self.start()

            self.terminal.clear()
            self.printer.generic(f'Cadeiras da Sala {room_id}', line=True)
            headers = ['Seat Code', 'Row', 'Column', 'State']

            seats_compacted = [
                [seat[2], seat[3], seat[4], seat[5]]
                for seat in seats
            ]

            self.printer.display_table(headers, seats_compacted)
            input('Voltar? [press enter]')
            self.start()

        except Exception as e:
            self.printer.error(f'Erro ao processar compra de ingresso: {e}')
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
