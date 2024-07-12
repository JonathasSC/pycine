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
            'Ver meus tickets',
            'Logout',
            'Sair'
        ]

        self.option_actions = {
            1: self.list_movies_in_playing,
            2: self.purchase_ticket,
            3: self.show_my_tickets,
            4: self.logout,
            5: self.exit
        }

    def start(self, is_admin: bool = False):
        self.logger.info('INICIANDO LOOP DE CLIENT VIEW')
        token: str = self.token.load_token()
        person_role: str = self.token.get_role_from_token(token)

        if person_role:
            while True:
                try:
                    self.terminal.clear()
                    self.update_options(is_admin)
                    option: int = self.choose_an_option(self.list_options)

                    if person_role == 'admin':
                        self.handle_admin_options(option)
                        break
                    elif person_role == 'client':
                        if self.handle_client_options(option):
                            self.start()
                        break

                except Exception as e:
                    self.printer.error(f'Erro ao iniciar tela publica: {e}')

                break

    def show_my_tickets(self):
        header = ['SEAT', 'MOVIE', 'TIME']

        token = self.token.load_token()
        person_id = self.token.person_id_from_token(token)

        try:
            tickets_list = self.tickets_crud.select_tickets_by_person_id(
                person_id)

            formated_list = []
            for ticket in tickets_list:
                seat_id = ticket[1]
                session_id = ticket[3]

                seat = self.seats_crud.select_seat_by_id(seat_id)
                seat_code = seat[2]

                session = self.session_crud.select_session_by_id(session_id)
                movie_id = session[2]
                start_time = session[4]
                movie = self.movies_crud.select_movie_by_id(movie_id)
                movie_title = movie[1]

                formated_list.append([seat_code, movie_title, start_time])

            self.printer.display_table(
                headers=header, table_data=formated_list)

        except Exception as e:
            self.printer.error(f'Erro ao mostrar os tickets: {e}')

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

                chosen_session: tuple = self.session_crud.select_session_by_id(
                    chosen_session_id)

                if not chosen_session:
                    self.handle_no_sessions_available()
                    return

                chosen_seat = self.process_ticket_purchase(chosen_session)
                chosen_movie: str = self.movies_crud.select_movie_by_id(movie_id)[
                    1]

                if self.confirm_purchase(chosen_movie=chosen_movie,
                                         session=chosen_session,
                                         chosen_seat=chosen_seat):
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

    def confirm_purchase(self, chosen_seat: str, session: tuple, chosen_movie: str):
        self.terminal.clear()
        self.printer.generic("Confirmação de Compra", line=True)

        seat: tuple = self.seats_crud.select_seat_by_room_id_and_seat_code(
            session[1], seat_code=chosen_seat)

        session_id: str = session[0]
        start_time: str = session[4]

        self.printer.generic(f"Filme: {chosen_movie}")
        self.printer.generic(f"Assento: {chosen_seat}")
        self.printer.generic(f"Horário: {start_time}")

        confirm_options = ['Sim, confirmar', 'Não, cancelar']
        option = self.inputs.choose_an_option(
            options=confirm_options, clear=False)

        if option == 1:
            self.process_ticket(seat, session_id)
            return True
        else:
            self.terminal.clear()
            self.printer.warning("Compra cancelada.")
            return False

    def process_ticket(self, seat, session_id):
        try:
            seat_id: str = seat[0]
            data = self.prepare_ticket_data(seat_id, session_id)

            self.tickets_crud.insert_ticket(data)
            self.seats_crud.update_seat_state(seat_id, 'sold')

        except Exception as e:
            self.printer.error(e)

    def prepare_ticket_data(self, seat_id, session_id):

        token = self.token.load_token()
        person_id = self.token.person_id_from_token(token)

        data = {
            'seat_id': seat_id,
            'person_id': person_id,
            'session_id': session_id,
        }

        return data

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
            f"{session[2].center(10, ' ')} | {session[1].center(10, ' ')} | {
                session[3].center(10, ' ')} | {session[0].center(10, ' ')}"
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
