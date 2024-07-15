from src.views.base_view import BaseView


class PurchaseView(BaseView):
    def __init__(self, manager):
        super().__init__()
        self.manager = manager
        token: str = self.token.load_token()
        self.person_id: str = self.token.person_id_from_token(token)

    def process_ticket(self, seat_id: str, person_id: str, session_id: str):
        try:
            data: dict = {'seat_id': seat_id,
                          'person_id': person_id, 'session_id': session_id}
            self.ticket_crud.insert_ticket(data)
            return True
        except Exception:
            self.printer.error('Erro ao iniciar Purchase View')
            return False

    def start(self):
        while True:
            token: str = self.token.load_token()
            person_id: str = self.token.person_id_from_token(token)
            movie_result = self.choose_movies()
            if movie_result is None:
                return
            movie_id, movie_name = movie_result
            session_result = self.choose_session()
            if session_result is None:
                return
            room_id, session_time, session_id = session_result
            seat_result = self.choose_seat(room_id, session_id)
            if seat_result is None:
                return
            seat_id, seat_code = seat_result
            if self.confirm_purchase(seat_code, session_time, movie_name):
                if self.process_ticket(seat_id, person_id, session_id):
                    self.printer.success('CHEGOU AQUI!')

    def choose_movies(self):
        self.logger.info('INICIANDO CHOOSE MOVIES')
        try:
            self.terminal.clear()
            sessions: list = self.session_crud.select_all_session_with_movies()
            movies_names = [session[6] for session in sessions]
            movies_ids = [session[5] for session in sessions]
            movie_option = self.inputs.choose_an_option(
                movies_names, 'Escolha um filme', True)
            if movie_option == 0:
                return None
            choose_movie_index = movie_option - 1
            movie_id = movies_ids[choose_movie_index]
            movie_name = movies_names[choose_movie_index]
            return movie_id, movie_name
        except Exception:
            self.printer.error('Excessão ao tentar escolher filmes')
            return None

    def choose_session(self):
        self.logger.info('INICIANDO CHOOSE SESSION')
        try:
            self.terminal.clear()
            sessions: list = self.session_crud.select_all_session_with_movies()

            sessions_id = [session[0] for session in sessions]
            rooms_id = [session[1] for session in sessions]
            session_times = [session[4] for session in sessions]

            sessions_formatted = [
                f"{session[2]} | {session[1]} | { session[4]}" for session in sessions]

            session_option = self.inputs.choose_an_option(
                sessions_formatted, 'Escolha uma sessão', True)

            if session_option == 0:
                return None

            session_id = sessions_id[session_option - 1]
            session_time = session_times[session_option - 1]
            room_id = rooms_id[session_option - 1]

            return room_id, session_time, session_id
        except Exception:
            self.printer.error('Excessão ao tentar escolher sessão')
            return None

    def choose_seat(self, room_id, session_id):
        session: str = self.session_crud.select_session_by_id(session_id)
        seats: list = self.seat_crud.select_seats_by_room_id(session[1])
        self.logger.info('INICIANDO CHOOSE SEAT')
        while True:
            try:
                seat_matrix: list = self.printer.create_seat_matrix(seats)
                self.printer.print_seat_matrix(seat_matrix)

                seat_code: str = input(
                    'Escolha um assento pelo código (ou digite "q" para voltar): ')

                if seat_code.lower() == 'q':
                    return None

                if self.validate_seat_choice(seats, seat_code) is None:
                    self.terminal.clear()
                    self.printer.error('Assento inválido, tente novamente')
                    continue

                seat: tuple = self.seat_crud.select_seat_by_room_id_and_seat_code(
                    room_id, seat_code)
                seat_id = seat[0]

                return seat_id, seat_code

            except Exception as e:
                self.printer.error(
                    f'Erro ao processar compra de ingresso: {e}')
                return None

    def validate_seat_choice(self, seats, chosen_seat):
        for seat in seats:
            if seat[2] == chosen_seat:
                return seat[5]
        return None

    def confirm_purchase(self, seat_code: str, session_time: str, movie_name: str):
        self.terminal.clear()

        self.printer.generic("Confirmação de Compra", line=True)
        self.printer.generic(f"Filme: {movie_name}")
        self.printer.generic(f"Assento: {seat_code}")
        self.printer.generic(f"Horário: {session_time}")

        confirm_options = ['Sim, confirmar', 'Não, cancelar']

        option = self.inputs.choose_an_option(
            options=confirm_options, clear=False)
        return option == 1
