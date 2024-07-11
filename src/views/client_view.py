from src.views.base_view import BaseView
from src.crud.movies_crud import MoviesCrud
from src.crud.sessions_crud import SessionsCrud

from src.crud.rooms_crud import RoomsCrud
from src.crud.seats_crud import SeatsCrud
from src.crud.tickets_crud import TicketsCrud


class ClientView(BaseView):
    def __init__(self):
        super().__init__()

        self.room_crud: RoomsCrud = RoomsCrud()
        self.seats_crud: SeatsCrud = SeatsCrud()
        self.movies_crud: MoviesCrud = MoviesCrud()
        self.tickets_crud: TicketsCrud = TicketsCrud()
        self.session_crud: SessionsCrud = SessionsCrud()

        self.back_view = None

        self.list_options: list = [
            'Ver filmes em exibição',
            'Comprar ingresso',
            'Logout',
            'Fechar'
        ]

    def start(self, is_admin: bool = False):
        self.logger.info('INICIANDO LOOP DE CLIENT VIEW')

        while True:
            try:
                self.terminal.clear()
                self.update_options(is_admin)
                option: int = self.choose_an_option(self.list_options)

                if is_admin:
                    self.handle_admin_options(option)
                    break
                else:
                    self.handle_client_options(option)
                    break

            except Exception as e:
                self.printer.error(f'Erro ao iniciar tela publica: {e}')

    def update_options(self, is_admin: bool):
        if is_admin and 'Voltar' not in self.list_options:
            self.list_options.append('Voltar')
            self.list_options.remove('Fechar')
            self.list_options.remove('Logout')

    def handle_admin_options(self, option: int):
        if option == 1:
            self.list_movies_in_playing()
        elif option == 2:
            self.purchase_ticket()
        elif option == 3 or option == 4:
            self.back()
        else:
            self.invalid_option()

    def handle_client_options(self, option):
        if option == 1:
            self.list_movies_in_playing()
        elif option == 2:
            self.purchase_ticket()
        elif option == 3:
            self.logout()
            return False
        elif option == 4:
            if self.close():
                return False
            else:
                self.start()
        else:
            self.invalid_option()
        return True

    def set_back_view(self, view):
        self.back_view = view

    def back(self):
        if self.back_view:
            self.back_view.start()
        else:
            self.printer.error('View anterior não definida')

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

                if self.confirm_purchase(chosen_movie=chosen_movie, session=chosen_session, chosen_seat=chosen_seat):
                    self.printer.success('COMPRA FEITA COM SUCESSO!')
                    break

            except IndexError:
                self.printer.generic(
                    "Erro ao acessar a lista de filmes ou sessões.")
            except Exception as e:
                self.printer.error(e)

            self.start()

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
            options=movies_names, text='Escolha uma sessão', cancel=True)
        if movie_option is None:
            self.start()

        return movies_ids[movie_option - 1]

    def choose_session(self, sessions):
        sessions_formatted = [
            f"{session[2].center(10, ' ')} | {session[1].center(10, ' ')} | {session[4].center(10, ' ')}"
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
        self.printer.warning("Nenhum filme disponível.")
        self.start()

    def confirm_close(self):
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

    def close(self):
        if self.confirm_close():
            return True
        return False
