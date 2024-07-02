import sqlite3
from src.queries.persons_queries import CREATE_PERSONS_TABLE
from src.queries.clients_queries import CREATE_CLIENTS_TABLE
from src.queries.admins_queries import CREATE_ADMINS_TABLE
from src.queries.movies_queries import CREATE_MOVIES_TABLE, DELETE_ALL_MOVIES
from src.queries.rooms_queries import CREATE_ROOMS_TABLE, DELETE_ALL_ROOMS
from src.queries.sessions_queries import CREATE_SESSION_TABLE, DELETE_ALL_SESSIONS
from src.queries.seats_queries import CREATE_SEATS_TABLE, DELETE_SEATS_TABLE, TRIGGER_CHECK_SEAT_CAPACITY


class Connection:
    def __init__(self, db_name: str = 'sqlite.db') -> None:
        self.db_name: str = db_name
        self.connection: sqlite3.Connection = None
        self.cursor: sqlite3.Cursor = None

        self.connect()
        self.create_database()

    def connect(self):
        self.connection = sqlite3.connect(self.db_name)
        self.cursor = self.connection.cursor()

    def close(self):
        if self.connection:
            self.connection.close()
        self.connection = None

    def create_database(self):
        self.cursor.execute(CREATE_SESSION_TABLE)
        self.cursor.execute(DELETE_ALL_SESSIONS)

        self.cursor.execute(CREATE_PERSONS_TABLE)
        self.cursor.execute(CREATE_CLIENTS_TABLE)
        self.cursor.execute(CREATE_ADMINS_TABLE)

        self.cursor.execute(DELETE_ALL_MOVIES)
        self.cursor.execute(CREATE_MOVIES_TABLE)

        self.cursor.execute(DELETE_ALL_ROOMS)
        self.cursor.execute(CREATE_ROOMS_TABLE)

        self.cursor.execute(DELETE_SEATS_TABLE)
        self.cursor.execute(CREATE_SEATS_TABLE)

        self.cursor.execute(TRIGGER_CHECK_SEAT_CAPACITY)
        self.connection.commit()
