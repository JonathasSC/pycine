from src.views.base_view import BaseView
from src.crud.movies_crud import MoviesCrud
from src.crud.sessions_crud import SessionsCrud

from src.crud.rooms_crud import RoomsCrud
from src.crud.seats_crud import SeatsCrud
from src.crud.tickets_crud import TicketsCrud
from typing import Optional


class ClientView(BaseView):
    def __init__(self):
        super().__init__()

        self.room_crud: RoomsCrud = RoomsCrud()
        self.seats_crud: SeatsCrud = SeatsCrud()
        self.movies_crud: MoviesCrud = MoviesCrud()
        self.tickets_crud: TicketsCrud = TicketsCrud()
        self.session_crud: SessionsCrud = SessionsCrud()

        self.list_options: list = [
            'Ver filmes em exibição',
            'Comprar ingresso',
            'Logout',
            'Sair'
        ]

        self.option_actions = {
            1: self.list_movies_in_playing,
            2: self.purchase_ticket,
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

    def purchase_ticket(self):
        while True:
            try:
                sessions_with_movies = self.session_crud.select_all_session_with_movies()
                if not sessions_with_movies:
                    self.handle_no_sessions_available()
                    return

                movie_id = self.choose_movie(sessions_with_movies)
                sessions_with_room_details = self.session_crud.select_sessions_with_room_details(
                    movie_id)
                if not sessions_with_room_details:
                    self.handle_no_sessions_available()
                    return

                chosen_session_id = self.choose_session(
                    sessions_with_room_details)
                session = self.session_crud.select_session_by_id(
                    chosen_session_id)
                if not session:
                    self.handle_no_sessions_available()
                    return

                chosen_seat = self.process_ticket_purchase(session)

                if self.confirm_purchase(chosen_seat, chosen_session_id):
                    self.printer.success('COMPRA FEITA COM SUCESSO!')
                    break

            except IndexError:
                self.printer.generic(
                    "Erro ao acessar a lista de filmes ou sessões.")
            except Exception as e:
                self.printer.error(e)

            self.start()

    def handle_no_sessions_available(self):
        self.terminal.clear()
        self.printer.warning("Nenhum filme disponível.")
        self.start()

    def confirm_purchase(self, chosen_seat, chosen_session_id):
        self.terminal.clear()
        self.printer.generic("Confirmação de Compra", line=True)
        self.printer.generic(f"Assento escolhido: {chosen_seat}")
        self.printer.generic("Confirmar sua compra?")

        confirm_options = ['Sim, confirmar', 'Não, cancelar']
        option = self.inputs.choose_an_option(options=confirm_options)

        if option == 1:
            self.process_ticket(chosen_seat, chosen_session_id)
            return True
        else:
            self.terminal.clear()
            self.printer.warning("Compra cancelada.")
            return False

    def process_ticket(self, seat_id, session_id):
        try:
            data = self.prepare_ticket_data(seat_id, session_id)
            self.tickets_crud.insert_ticket(data)
        except Exception as e:
            self.printer.error(e)

    def prepare_ticket_data(self, seat_id, session_id):
        token = self.token.load_token()
        person_id = self.token.person_id_from_token(token)
        room_id = self.seats_crud.get_seat_by_id(seat_id)
        return {
            'session_id': session_id,
            'person_id': person_id,
            'seat_id': seat_id,
            'room_id': room_id
        }

    def choose_movie(self, sessions):
        movies_names = [session[6] for session in sessions]
        movies_ids = [session[5] for session in sessions]

        self.terminal.clear()
        movie_option = self.inputs.choose_an_option(
            options=movies_names, text='Escolha uma sessão', cancel=True)
        if movie_option is None:
            self.start()

        return movies_ids[movie_option - 1]

    def choose_session(self, sessions):
        sessions_formatted = [
            f'{session[2].center(10, " ")} | {session[1].center(10, " ")} | {
                session[3].center(10, " ")} | {session[0].center(10, " ")}'
            for session in sessions
        ]

        sessions_ids = [session[5] for session in sessions]
        session_option = self.choose_an_option(
            sessions_formatted, 'Escolha uma sessão', True)
        if session_option is None:
            self.start()
        return sessions_ids[session_option - 1]

    def show_seats_in_room(self, seats):
        seat_matrix = self.create_seat_matrix(seats)
        self.print_seat_matrix(seat_matrix)

    def create_seat_matrix(self, seats):
        max_row = max(seat[3] for seat in seats) + 1
        max_col = max(seat[4] for seat in seats) + 1

        seat_matrix = [['' for _ in range(max_col)] for _ in range(max_row)]
        for seat in seats:
            row, col, state, seat_code = seat[3], seat[4], seat[5], seat[2]
            color_code = self.get_seat_color(state)
            seat_matrix[row][col] = f"{color_code}[{seat_code}]\033[0m"
        return seat_matrix

    def get_seat_color(self, state):
        return {
            'available': '\033[92m',
            'reserved': '\033[93m',
            'sold': '\033[91m'
        }.get(state, '\033[0m')

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
                    'Escolha um assento pelo código (ou digite "q" para voltar): ')
                if chosen_seat.lower() == 'q':
                    self.start()
                    return

                seat_state = self.validate_seat_choice(seats, chosen_seat)
                if self.handle_seat_selection(seat_state, chosen_seat):
                    break
            except Exception as e:
                self.printer.error(
                    f'Erro ao processar compra de ingresso: {e}')

        return chosen_seat

    def handle_seat_selection(self, seat_state, chosen_seat):
        if seat_state == 'available':
            self.terminal.clear()
            self.printer.success(f'Você escolheu o assento {chosen_seat}.')
            return True
        elif seat_state == 'reserved':
            self.terminal.clear()
            self.printer.error(f'O assento {chosen_seat} está reservado.')
        elif seat_state == 'sold':
            self.terminal.clear()
            self.printer.error(f'O assento {chosen_seat} está vendido.')
        else:
            self.terminal.clear()
            self.printer.error('Código de assento inválido.')
        return False

    def validate_seat_choice(self, seats, chosen_seat):
        for seat in seats:
            if seat[2] == chosen_seat:
                return seat[5]
        return None

    def list_movies_in_playing(self):
        while True:
            try:
                movies_list = self.session_crud.select_all_session_with_movies()
                if not movies_list:
                    self.handle_no_sessions_available()
                    return

                self.display_movies(movies_list)
            except Exception as e:
                print(f'Erro ao mostrar filmes {e}')
            break

    def display_movies(self, movies_list):
        headers: list = ['NAME', 'GENRE', 'DURATION', 'SYNOPSIS']

        self.terminal.clear()
        self.printer.generic(
            text='Filmes em cartaz',
            line=True

        )

        movies_compacted = [
            [movie[6], movie[7], movie[8], f'{str(movie[9])[:50]}...'] for movie in movies_list
        ]

        self.printer.display_table(headers, movies_compacted)
        self.start()
