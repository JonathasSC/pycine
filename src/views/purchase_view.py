from src.views.base_view import BaseView


class PurchaseView(BaseView):
    def __init__(self, manager):
        super().__init__()

        self.manager = manager
        self.sessions: list = self.session_crud.select_all_session_with_movies()

        self.room_id: str = ''
        self.seat_id: str = ''
        self.movie_id: str = ''
        self.person_id: str = ''
        self.session_id: str = ''

        self.seat_code: str = ''
        self.movie_name: str = ''
        self.session_time: str = ''

        token: str = self.token.load_token()
        self.person_id: str = self.token.person_id_from_token(token)

    def process_ticket(
            self,
            seat_id: str,
            person_id: str,
            session_id: str):

        try:
            data: dict = {}
            data['seat_id'] = seat_id
            data['person_id'] = person_id
            data['session_id'] = session_id
            self.ticket_crud.insert_ticket(data)
            return True

        except Exception:
            self.printer.error('Erro ao iniciar Purchase View')

    def start(self):
        try:
            self.choose_movies()
        except Exception:
            self.printer.error('Erro ao iniciar Purchase View')

    def choose_movies(self):
        self.logger.info('INICIANDO CHOOSE SESSION')

        if self.sessions:
            try:
                self.terminal.clear()

                sessions: list = self.session_crud.select_all_session_with_movies()
                movies_names = [session[6] for session in sessions]
                movies_ids = [session[5] for session in sessions]

                movie_option = self.inputs.choose_an_option(
                    movies_names,
                    'Escolha um filme',
                    True
                )

                choose_movie_index = movie_option - 1
                person_role: str = self.person_crud.get_person_role(
                    self.person_id)

                if movie_option == 0 and person_role == 'client':
                    self.manager.client_view.start()
                    return

                if movie_option == 0 and person_role == 'admin':
                    self.manager.client_view.start()
                    return

                self.movie_id = movies_ids[choose_movie_index]
                self.movie_name = movies_names[choose_movie_index]

                self.choose_session()

            except Exception:
                self.printer.error('Excessão ao tentar escolher filmes')

        return None

    def choose_session(self):
        self.logger.info('INICIANDO CHOOSE SESSION')

        if self.sessions:
            try:
                self.terminal.clear()

                sessions_id = [session[0] for session in self.sessions]
                rooms_id = [session[1] for session in self.sessions]
                session_times = [session[4] for session in self.sessions]

                sessions_formatted = [
                    f"{session[2]} | {session[1]} | { session[4]}"
                    for session in self.sessions
                ]

                session_option = self.inputs.choose_an_option(
                    sessions_formatted,
                    'Escolha uma sessão',
                    True
                )

                if session_option == 0:
                    self.manager.purchase_view.choose_movies()

                self.session_id = sessions_id[session_option - 1]
                self.session_time = session_times[session_option - 1]
                self.room_id = rooms_id[session_option - 1]

                self.choose_seat()

            except Exception:
                self.printer.error('Excessão ao tentar escolher filmes')

        return None

    def choose_seat(self):
        session: str = self.session_crud.select_session_by_id(self.session_id)
        seats: list = self.seat_crud.select_seats_by_room_id(
            session[1])

        self.logger.info('INICIANDO CHOOSE SEAT')
        while True:
            try:
                seat_matrix: list = self.printer.create_seat_matrix(seats)
                self.printer.print_seat_matrix(seat_matrix)

                self.seat_code: str = input(
                    'Escolha um assento pelo código (ou digite "q" para voltar): '
                )

                if self.seat_code.lower() == 'q':
                    self.choose_session()
                    return

                if self.validate_seat_choice(seats, self.seat_code) == None:
                    self.terminal.clear()
                    self.printer.error('Assento inválido, tente novamente')
                    self.terminal.clear()
                    continue

                if self.confirm_purchase(self.seat_code, self.session_time, self.movie_name) == None:
                    self.manager.purchase_view.choose_seat()

                seat: tuple = self.seat_crud.select_seat_by_room_id_and_seat_code(
                    self.room_id,
                    self.seat_code
                )

                self.seat_id = seat[0]

                if self.process_ticket(self.seat_id, self.person_id, self.session_id):
                    self.seat_crud.update_seat_state(self.seat_id, 'sold')
                    self.printer.success('TICKET COMPRADO COM SUCESSO!')

            except Exception as e:
                self.printer.error(
                    f'Erro ao processar compra de ingresso: {e}')

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

        if option == 1:
            return True
        else:
            return False
