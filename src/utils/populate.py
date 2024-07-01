from src.crud.persons_crud import PersonsCrud
from src.crud.admins_crud import AdminsCrud
from src.crud.clients_crud import ClientsCrud

from src.crud.sessions_crud import SessionsCrud
from src.crud.rooms_crud import RoomsCrud
from src.crud.movies_crud import MoviesCrud
from faker import Faker


class Populate:
    def __init__(self) -> None:
        self.populate_range: int = 10
        self.person_crud: PersonsCrud = PersonsCrud()
        self.admin_crud: AdminsCrud = AdminsCrud()
        self.client_crud: ClientsCrud = ClientsCrud()

        self.rooms_crud: RoomsCrud = RoomsCrud()
        self.movies_crud: MoviesCrud = MoviesCrud()
        self.session_crud: SessionsCrud = SessionsCrud()

    def populate_persons(self):
        for n in range(self.populate_range):
            data = {
                'name': Faker().name(),
                'email': Faker().email(),
                'password': Faker().password(),
            }
            self.person_crud.insert_person(data)

    def populate_admins(self):
        for n in range(self.populate_range):
            data = {
                'name': Faker().name(),
                'email': Faker().email(),
                'password': Faker().password(),
            }

            person_id: str = self.person_crud.insert_person(data)
            self.admin_crud.insert_admin(person_id)

    def populate_clients(self):
        for n in range(self.populate_range):
            data = {
                'name': Faker().name(),
                'email': Faker().email(),
                'password': Faker().password(),
            }

            person_id: str = self.person_crud.insert_person(data)
            self.client_crud.insert_client(person_id)

    def populate_movies(self):
        for n in range(self.populate_range):
            data = {
                'name': Faker().name(),
                'genre': 'ação',
                'duration': Faker().time(pattern='%H:%M:%S'),
                'synopsis': Faker().text()
            }

            self.movies_crud.insert_movie(data)

    def populate_rooms(self):
        for n in range(self.populate_range):
            data = {
                'name': Faker().name(),
                'genre': 'ação',
                'duration': Faker().time(pattern='%H:%M:%S'),
                'synopsis': Faker().text()
            }

            self.movies_crud.insert_movie(data)
