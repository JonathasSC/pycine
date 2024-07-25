from src.views.base_view import BaseView
from src.utils.validators import validate_seat_choice
from typing import Optional


class PurchaseView(BaseView):

    def __init__(self, manager):
        super().__init__()
        self.manager = manager

    def start(self):
        token: str = self.token.load_token()
        person_role: str = self.token.get_role_from_token(token)
        person_id: str = self.token.person_id_from_token(token)

        while True:
            try:
                chosen_movie: tuple = self.choose_movie()
                self.terminal.clear()
                if not chosen_movie:
                    break

                chosen_movie_id: str = chosen_movie[0]
                session: tuple = self.choose_session(chosen_movie_id)
                self.terminal.clear()
                if not session:
                    break

                chosen_room_id: str = session[1]
                seat: tuple = self.choose_seat(chosen_room_id)
                self.terminal.clear()
                if not seat:
                    break

                ticket: tuple = self.process_ticket(seat, session, person_id)
                self.terminal.clear()
                if not ticket:
                    break

                self.terminal.clear()
                self.printer.success(
                    'COMPRA EFEITUADA COM SUCESSO, VOLTE SEMPRE!')

            except Exception as e:
                raise e

        if person_role == 'client':
            self.manager.client_view.start()

        elif person_role == 'admin':
            self.manager.client_view.start()

    def choose_movie(self) -> Optional[tuple]:
        self.terminal.clear()
        movies: list = self.session_crud.select_all_session_with_movies()
        movies_names = [movie[6] for movie in movies]

        option: str = self.choose_an_option(
            options=movies_names,
            text='Escolha um filme',
            cancel=True
        )

        if not option:
            return

        chosen_movie_name = movies_names[option - 1]
        movie: tuple = self.movie_crud.select_movie_by_name(chosen_movie_name)

        return movie

    def choose_session(self, movie_id) -> Optional[tuple]:
        self.terminal.clear()
        sessions: list = self.session_crud.select_sessions_by_movie_id_with_room_details(
            movie_id)

        options_formated = [
            f'{session[0]} | {session[1]} | {session[2]} | {session[3]}' for session in sessions]

        sessions_id: list = [session[5] for session in sessions]

        option = self.choose_an_option(
            options=options_formated,
            text='Escolha uma sessão',
            cancel=True
        )

        if not option:
            self.terminal.clear()
            return

        chosen_session_id = sessions_id[option - 1]
        session: tuple = self.session_crud.select_session_by_id(
            chosen_session_id)

        self.terminal.clear()
        return session

    def choose_seat(self, room_id) -> Optional[tuple]:
        while True:
            self.terminal.clear()
            seats: list = self.seat_crud.select_seats_by_room_id(room_id)
            seat_matrix: list = self.printer.create_seat_matrix(seats)
            self.printer.print_seat_matrix(seat_matrix)

            seat_code: str = input(
                'Escolha um assento pelo código (ou digite "q" para voltar): ')

            if seat_code.lower() == 'q':
                self.terminal.clear()
                return None

            if validate_seat_choice(seats, seat_code):
                seat: tuple = self.seat_crud.select_seat_by_room_id_and_seat_code(
                    room_id,
                    seat_code)

                self.terminal.clear()
                return seat

            self.terminal.clear()
            self.printer.error(
                'Assento indisponivel, escolha outro',
                timer=True)
            self.terminal.clear()

    def process_ticket(self,
                       seat: tuple,
                       session: tuple,
                       person_id: str) -> Optional[tuple]:

        self.terminal.clear()
        seat_code: str = seat[2]
        session_time: str = session[4]
        movie_name: str = self.movie_crud.select_movie_by_id(session[2])[1]

        self.printer.generic("Revise seu ticket", line=True)
        self.printer.generic(f"Filme: {movie_name}")
        self.printer.generic(f"Assento: {seat_code}")
        self.printer.generic(f"Horário: {session_time}")

        confirm_options = ['Sim, confirmar']
        option: str = self.choose_an_option(
            text='Finalize sua compra!',
            options=confirm_options,
            cancel=True
        )

        if not option:
            self.terminal.clear()
            return

        data: dict = {}
        data['seat_id'] = seat[0]
        data['person_id'] = person_id
        data['session_id'] = session[0]

        ticket_id: str = self.ticket_crud.insert_ticket(data)
        ticket: tuple = self.ticket_crud.select_ticket_by_id(ticket_id)

        self.terminal.clear()
        return ticket
