from src.database.conn import Connection
from src.queries.persons_queries import INSERT_PERSON, SELECT_PERSON_BY_EMAIL
from src.utils.uuid import UUID


class PersonsCrud:
    def __init__(self, conn: Connection = Connection()):
        self.uuid: UUID = UUID()
        self.conn = conn

    def insert_person(self, data: dict):
        try:
            person_id: str = self.uuid.smaller_uuid()
            data_list: list = list(data.values())
            data_list.insert(0, person_id)

            self.conn.cursor.execute(INSERT_PERSON, data_list)
            self.conn.connection.commit()

            return True

        except Exception as e:
            return e

    def select_person_by_email(self, email: str):
        try:
            self.conn.cursor.execute(SELECT_PERSON_BY_EMAIL, [email])
            person: tuple = self.conn.cursor.fetchone()

            return person

        except Exception:
            return None
