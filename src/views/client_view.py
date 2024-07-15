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

        self.list_options: list = [
            'Ver filmes em exibição',
            'Ver meus tickets',
            'Comprar ingresso',
            'Logout',
            'Fechar'
        ]

    def start(self, is_admin: bool = False):
        while True:
            self.logger.info('INICIANDO LOOP DE CLIENT VIEW')
            token: str = self.token.load_token()
            person_role: str = self.token.get_role_from_token(token)

            if person_role:
                try:
                    self.terminal.clear()
                    self.update_options(is_admin)
                    option: int = self.choose_an_option(self.list_options)

                    if person_role == 'admin':
                        self.handle_admin_options(option)
                        break
                    elif person_role == 'client':
                        self.logger.info('INICIANDO HANDLE DE CLIENT VIEW')
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
            self.show_my_tickets()
            self.start()

        elif option == 3:
            self.manager.purchase_view.start()

        elif option == 4:
            self.manager.admin_view.start()

        else:
            self.invalid_option()

    def handle_client_options(self, option):
        match option:
            case 1:
                self.list_movies_in_playing()
            case 2:
                self.show_my_tickets()
            case 3:
                self.logger.info('INICIANDO PURCHASE VIEW')
                self.manager.purchase_view.start()
            case 4:
                self.logout()
                self.manager.home_view.start()
            case 5:
                if self.close():
                    return
                self.start()
            case _:
                self.invalid_option()
                self.start()

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
            self.start()

        except Exception as e:
            self.printer.error(f'Erro ao mostrar os tickets: {e}')

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
