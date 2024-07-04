import sqlite3
from src.queries.persons_queries import CREATE_PERSONS_TABLE
from src.queries.clients_queries import CREATE_CLIENTS_TABLE
from src.queries.admins_queries import CREATE_ADMINS_TABLE
from src.queries.movies_queries import CREATE_MOVIES_TABLE, DELETE_ALL_MOVIES
from src.queries.rooms_queries import CREATE_ROOMS_TABLE, DELETE_ALL_ROOMS
from src.queries.sessions_queries import CREATE_SESSION_TABLE, DELETE_ALL_SESSIONS
from src.queries.seats_queries import CREATE_SEATS_TABLE, DELETE_ALL_SEATS, TRIGGER_CHECK_SEAT_CAPACITY
from src.queries.tickets_queries import CREATE_TICKETS_TABLE

from src.utils.logger import Logger


class Connection:
    def __init__(self, db_name: str = 'sqlite.db', auto_connect: bool = True) -> None:
        self.logger: Logger = Logger()

        self.db_name: str = db_name
        self.connection: sqlite3.Connection = None
        self.cursor: sqlite3.Cursor = None
        if auto_connect:
            self.connect()

    def connect(self):
        self.connection = sqlite3.connect(self.db_name)
        self.cursor = self.connection.cursor()
        self.logger.info('ABRINDO CONEXAO COM BANCO DE DADOS')

    def close(self):
        if self.connection:
            self.connection.close()
            self.logger.info('FECHANDO CONEXAO COM BANCO DE DADOS')
        self.connection = None

    def delete_data(self):
        self.connect()

        self.cursor.execute(DELETE_ALL_SESSIONS)
        self.cursor.execute(DELETE_ALL_MOVIES)
        self.cursor.execute(DELETE_ALL_ROOMS)
        self.cursor.execute(DELETE_ALL_SEATS)

        self.connection.commit()
        self.close()

        self.logger.info('DELETANDO DADOS')

    def create_database(self):
        self.connect()

        self.logger.info('CRIANDO TABELAS DE USUARIOS')
        self.cursor.execute(CREATE_PERSONS_TABLE)
        self.cursor.execute(CREATE_CLIENTS_TABLE)
        self.cursor.execute(CREATE_ADMINS_TABLE)

        self.logger.info('CRIANDO TABELAS ABSTRATAS')
        self.cursor.execute(CREATE_SESSION_TABLE)
        self.cursor.execute(CREATE_MOVIES_TABLE)
        self.cursor.execute(CREATE_ROOMS_TABLE)
        self.cursor.execute(CREATE_SEATS_TABLE)
        self.cursor.execute(CREATE_TICKETS_TABLE)

        self.logger.info('CRIANDO TRIGGERS')
        self.cursor.execute(TRIGGER_CHECK_SEAT_CAPACITY)
        self.connection.commit()
        self.close()
