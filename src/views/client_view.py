from src.views.base_view import BaseView
from src.crud.movies_crud import MoviesCrud
from src.crud.sessions_crud import SessionsCrud

from src.crud.rooms_crud import RoomsCrud
from src.crud.seats_crud import SeatsCrud


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
            'Logout',
            'Sair'
        ]

        self.option_actions = {
            1: self.list_movies_in_playing,
            2: self.buy_ticket,
            3: self.logout,
            4: self.exit
        }

    def start(self):
        self.logger.info('INICIANDO LOOP DE CLIENT VIEW')
        while True:
            try:
                self.terminal.clear()
                option: int = self.choose_an_option(self.list_options)
                self.execute_option(self.option_actions, option)

            except Exception as e:
                self.printer.error(f'Erro ao iniciar tela publica: {e}')

            self.logger.info('PARANDO LOOP DE CLIENT VIEW')
            break

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

                session: tuple = self.session_crud.select_session_by_id(
                    chosen_session_id
                )

                if not session:
                    self.terminal.clear()
                    self.printer.warning("Nenhuma sessão disponível.")
                    self.start()

                self.process_ticket_purchase(session)

            except IndexError:
                self.printer.generic(
                    "Erro ao acessar a lista de filmes ou sessões."
                )

            except Exception as e:
                self.printer.error(e)

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

    def show_seats_in_room(self, seats):
        seat_matrix = self.create_seat_matrix(seats)
        self.print_seat_matrix(seat_matrix)

    def create_seat_matrix(self, seats):
        max_row = max(seat[3] for seat in seats) + 1
        max_col = max(seat[4] for seat in seats) + 1

        seat_matrix = [['' for _ in range(max_col)] for _ in range(max_row)]

        for seat in seats:
            row = seat[3]
            col = seat[4]
            state = seat[5]
            seat_code = seat[2]

            match state:
                case 'available':
                    color_code = '\033[92m'
                case 'reserved':
                    color_code = '\033[93m'
                case 'sold':
                    color_code = '\033[91m'
                case _:
                    color_code = '\033[0m'

            seat_matrix[row][col] = f"{color_code}[{seat_code}]\033[0m"

        return seat_matrix

    def print_seat_matrix(self, seat_matrix):
        self.terminal.clear()
        print(' tela '.center(len(seat_matrix[0]) * 5, '-'))

        for row in seat_matrix:
            print(" ".join(row))

    def process_ticket_purchase(self, session):
        while True:
            try:
                room_id = session[1]
                seats = self.seats_crud.get_seats_by_room_id(room_id)
                self.show_seats_in_room(seats)
                chosen_seat = input(
                    'Escolha um assento pelo código (ou digite "q" para voltar): '
                )

                if chosen_seat.lower() == 'q':
                    self.start()
                    return

                seat_state = self.validate_seat_choice(seats, chosen_seat)

                match seat_state:
                    case 'available':
                        self.terminal.clear()
                        self.printer.success(
                            f'Você escolheu o assento {chosen_seat}.')
                        break

                    case 'reserved':
                        self.terminal.clear()
                        self.printer.error(
                            f'O assento {chosen_seat} está reservado.')
                        self.process_ticket_purchase(session)

                    case 'sold':
                        self.terminal.clear()
                        self.printer.error(
                            f'O assento {chosen_seat} está vendido.')
                        self.process_ticket_purchase(session)

                    case _:
                        self.terminal.clear()
                        self.printer.error('Código de assento inválido.')
                        self.process_ticket_purchase(session)

                input('Voltar? [press enter]')
                self.start()

            except Exception as e:
                self.printer.error(
                    f'Erro ao processar compra de ingresso: {e}')

    def validate_seat_choice(self, seats, chosen_seat):
        for seat in seats:
            if seat[2] == chosen_seat:
                return seat[5]
        return None

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
                self.start()

            except Exception as e:
                print(f'Erro ao mostrar filmes {e}')

            break
