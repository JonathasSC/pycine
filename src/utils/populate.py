import random
from src.crud.seats_crud import SeatsCrud
from src.crud.rooms_crud import RoomsCrud
from src.crud.admins_crud import AdminsCrud
from src.crud.movies_crud import MoviesCrud
from src.crud.clients_crud import ClientsCrud
from src.crud.persons_crud import PersonsCrud
from src.crud.sessions_crud import SessionsCrud

from faker import Faker
from datetime import datetime, timedelta


class Populate:
    def __init__(self) -> None:
        self.populate_range: int = 10

        self.rooms_crud: RoomsCrud = RoomsCrud()
        self.seats_crud: SeatsCrud = SeatsCrud()
        self.admin_crud: AdminsCrud = AdminsCrud()
        self.movies_crud: MoviesCrud = MoviesCrud()
        self.person_crud: PersonsCrud = PersonsCrud()
        self.client_crud: ClientsCrud = ClientsCrud()
        self.session_crud: SessionsCrud = SessionsCrud()

    def populate_persons(self):
        for _ in range(self.populate_range):
            data = {
                'name': Faker().name(),
                'email': Faker().email(),
                'password': Faker().password(),
            }
            self.person_crud.insert_person(data)

    def populate_admins(self):
        for _ in range(self.populate_range):
            data = {
                'name': Faker().name(),
                'email': Faker().email(),
                'password': Faker().password(),
            }

            person_id: str = self.person_crud.insert_person(data)
            self.admin_crud.insert_admin(person_id)

    def populate_clients(self):
        for _ in range(self.populate_range):
            data = {
                'name': Faker().name(),
                'email': Faker().email(),
                'password': Faker().password(),
            }

            person_id: str = self.person_crud.insert_person(data)
            self.client_crud.insert_client(person_id)

    def populate_movies(self):
        for _ in range(self.populate_range):
            data = {
                'name': Faker().name(),
                'genre': 'ação',
                'duration': Faker().time(pattern='%H:%M:%S'),
                'synopsis': Faker().text()
            }

            self.movies_crud.insert_movie(data)

    def populate_rooms(self):
        for _ in range(self.populate_range):
            data = {
                'name': self.generate_pattern(),
                'rows': 10,
                'columns': 10,
                'type': 'vip'
            }

            self.rooms_crud.insert_room(data)

    def populate_sessions(self):
        rooms_id_list: list = []
        movies_id_list: list = []

        for _ in range(self.populate_range):
            data = {
                'name': Faker().name(),
                'genre': 'ação',
                'duration': Faker().time(pattern='%H:%M:%S'),
                'synopsis': Faker().text()
            }

            movies_id_list.append(self.movies_crud.insert_movie(data))

        for _ in range(self.populate_range):
            data = {
                'name': self.generate_pattern(),
                'rows': 10,
                'columns': 10,
                'type': 'vip'
            }

            rooms_id_list.append(self.rooms_crud.insert_room(data))

        for n in range(self.populate_range):
            now = datetime.now()
            future_date = (now + timedelta(days=random.randint(1, 30))).date()
            future_time = (now + timedelta(hours=random.randint(1, 12))).time()

            data = {
                'price': '25.50',
                'room_id': rooms_id_list[n],
                'movie_id': movies_id_list[n],
                'start_date': future_date,
                'start_time': future_time
            }

            self.session_crud.insert_session(data)

    def populate_seats(self):
        rooms = self.rooms_crud.select_all_rooms()
        for room in rooms:
            self.seats_crud.insert_seats_by_room(room)

    def generate_pattern(self):
        letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
        number = random.randint(1, 99)
        return random.choice(letters) + str(number)

    def populate_all(self):
        self.populate_persons()
        self.populate_clients()

        self.populate_rooms()
        self.populate_movies()
        self.populate_sessions()
        self.populate_seats()
