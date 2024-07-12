from src.views.base_view import BaseView
from src.crud.movies_crud import MoviesCrud
from src.crud.sessions_crud import SessionsCrud

from src.crud.rooms_crud import RoomsCrud
from src.crud.seats_crud import SeatsCrud
from src.crud.tickets_crud import TicketsCrud


class ClientView(BaseView):
    def __init__(self, manager):
        super().__init__()

        self.manager = manager

        self.room_crud: RoomsCrud = RoomsCrud()
        self.seats_crud: SeatsCrud = SeatsCrud()
        self.movies_crud: MoviesCrud = MoviesCrud()
        self.tickets_crud: TicketsCrud = TicketsCrud()
        self.session_crud: SessionsCrud = SessionsCrud()

        self.back_view = None

        self.list_options: list = [
            'Ver filmes em exibição',
            'Ver meus tickets',
            'Comprar ingresso',
            'Logout',
            'Fechar'
        ]

    def choose_movies(self, sessions: list):
        try:
            movies_names = [session[6] for session in sessions]
            movies_ids = [session[5] for session in sessions]

            self.terminal.clear()
            movie_option = self.inputs.choose_an_option(
                options=movies_names,
                text='Escolha uma sessão',
                cancel=True
            )

            if movie_option != 0 and movie_option != None:
                return movies_ids[movie_option - 1]
            elif movie_option == 0:
                return None

        except Exception:
            self.printer.error('Excessão ao tentar escolher filmes')

    def choose_sessions(self, sessions: list):
        sessions_ids: list = [
            session[0] for session in sessions
        ]

        room_ids: list = [
            session[1] for session in sessions
        ]

        room_type: list = []

        for room_id in room_ids:
            room: str = self.room_crud.select_by_room_id(room_id)
            room_type.append(room[4])

        formatted: list = []

        for index in range(0, len(sessions)):
            line = f"{room_type[index]} | {
                sessions[index][4]} | {sessions[index][3]}"
            formatted.append(line)

        self.terminal.clear()

        session_option = self.inputs.choose_an_option(
            options=formatted,
            text='Escolha uma sessão',
            cancel=True)

        if session_option is None:
            self.start()

        return sessions_ids[session_option - 1]

    # def choose_seats(self, room_id: str):
    #     try:
    #         seats: list = self.seats_crud.select_seats_by_room_id(room_id)
    #         self.create_seat_matrix(seats)
    #         self.print_seat_matrix(seat_matrix)

    def process_purchase(self):
        sessions = self.session_crud.select_all_session_with_movies()
        movie_id: str = self.choose_movies(sessions)
        session_id: str = self.choose_sessions(sessions)
        room_id: str = self.session_crud.se
        seat_id: str = self.choose_seat(sessions)

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

    def update_options(self, is_admin: bool):
        if is_admin and 'Voltar' not in self.list_options:
            self.list_options.append('Voltar')
            self.list_options.remove('Fechar')
            self.list_options.remove('Logout')

    def handle_admin_options(self, option: int):
        if option == 1:
            self.list_movies_in_playing()

        elif option == 2:
            self.show_my_tickets()
            self.start()

        elif option == 3:
            self.process_purchase()

        elif option == 4:
            self.manager.admin_view.start()

        else:
            self.invalid_option()

    def handle_client_options(self, option):

        if option == 1:
            self.list_movies_in_playing()

        elif option == 2:
            self.show_my_tickets()
            self.start()

        elif option == 3:
            self.process_purchase()

        elif option == 4:
            self.logout()
            self.manager.home_view.start()
            return False

        elif option == 5:
            if self.close():
                return False
            else:
                return True
        else:
            self.invalid_option()
        return True

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
                    return False

                movie_id = self.choose_movie(sessions_with_movies)

                if movie_id == 0:
                    return False

                if not movie_id:
                    self.handle_no_sessions_available()
                    return False

                sessions_with_room_details = self.session_crud.select_sessions_with_room_details(
                    movie_id)

                if not sessions_with_room_details:
                    self.handle_no_sessions_available()
                    return False

                chosen_session_id = self.choose_session(
                    sessions_with_room_details)
                if not chosen_session_id:
                    self.handle_no_sessions_available()
                    return False

                chosen_session = self.session_crud.select_session_by_id(
                    chosen_session_id)
                if not chosen_session:
                    self.handle_no_sessions_available()
                    return False

                while True:
                    chosen_seat = self.process_ticket_purchase(chosen_session)
                    if not chosen_seat:
                        if self.confirm_cancel("Deseja cancelar a compra?"):
                            return
                        else:
                            continue

                    chosen_movie = self.movies_crud.select_movie_by_id(movie_id)[
                        1]

                    if self.confirm_purchase(chosen_movie=chosen_movie, session=chosen_session, chosen_seat=chosen_seat):
                        self.printer.success('COMPRA FEITA COM SUCESSO!')
                        break

            except IndexError:
                self.printer.generic(
                    "Erro ao acessar a lista de filmes ou sessões.")
            except Exception as e:
                self.printer.error(e)

            if not self.confirm_continue("Deseja continuar comprando?"):
                return

    def confirm_purchase(self, chosen_seat: str, session: tuple, chosen_movie: str):
        self.terminal.clear()
        self.printer.generic("Confirmação de Compra", line=True)

        session_id: str = session[0]
        start_time: str = session[4]
        self.printer.generic(f"Filme: {chosen_movie}")
        self.printer.generic(f"Assento: {chosen_seat}")
        self.printer.generic(f"Horário: {start_time}")

        confirm_options = ['Sim, confirmar', 'Não, cancelar']
        option = self.inputs.choose_an_option(
            options=confirm_options, clear=False)

        if option == 1:
            self.process_ticket(chosen_seat, session_id)
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
            options=movies_names,
            text='Escolha uma sessão',
            cancel=True
        )

        if movie_option != 0 and movie_option != None:
            return movies_ids[movie_option - 1]
        elif movie_option == 0:
            return 0

        return None

    def choose_session(self, sessions):
        sessions_formatted = [
            f"{session[2].center(10, ' ')} | {session[1].center(10, ' ')} | {
                session[4].center(10, ' ')}"
            for session in sessions
        ]
        sessions_ids = [session[0] for session in sessions]

        self.terminal.clear()
        session_option = self.inputs.choose_an_option(
            options=sessions_formatted, text='Escolha uma sessão', cancel=True)
        if session_option is None:
            self.start()

        return sessions_ids[session_option - 1]

    def process_ticket_purchase(self, chosen_session):
        room_id = chosen_session[3]
        seats = self.seats_crud.select_seats_by_room_id(room_id)
        seats_formatted = [f"{seat[0]} - {seat[1]}" for seat in seats]

        self.terminal.clear()
        chosen_seat_option = self.inputs.choose_an_option(
            options=seats_formatted, text='Escolha seu assento', cancel=True)
        if chosen_seat_option is None:
            self.start()

        return seats[chosen_seat_option - 1][0]

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

    def handle_no_movies_available(self):
        self.terminal.clear()
        self.printer.generic("Nenhum filme em exibição no momento", line=True)
        self.printer.generic("Voltando para o início", timer=True)
        self.start()

    def handle_no_sessions_available(self):
        self.terminal.clear()
        self.printer.warning("Nenhuma sessão disponível.")

    def close(self):
        self.terminal.clear()

        confirm_options = ['Sim', 'Não']
        option = self.choose_an_option(
            confirm_options, text='Realmente deseja sair?')

        if option == 1:
            self.terminal.clear()
            self.printer.generic('Fechado...', line=True, timer=True)
            self.terminal.clear()
            return True

        return False

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
