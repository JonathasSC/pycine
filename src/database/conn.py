import sqlite3
from src.queries.persons_queries import CREATE_PERSONS_TABLE
from src.queries.admins_queries import CREATE_ADMINS_TABLE
from src.queries.clients_queries import CREATE_CLIENTS_TABLE


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
        self.cursor.execute(CREATE_PERSONS_TABLE)
        self.cursor.execute(CREATE_ADMINS_TABLE)
        self.cursor.execute(CREATE_CLIENTS_TABLE)
        self.connection.commit()
