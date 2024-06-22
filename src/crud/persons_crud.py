from src.database.conn import Connection
from src.queries.persons_queries import INSERT_PERSON, SELECT_PERSON_BY_EMAIL
from src.utils.uuid import UUID
from src.schemas.person_schemas import PersonCreate


class PersonsCrud:
    def __init__(self, conn: Connection = Connection()):
        self.uuid: UUID = UUID()
        self.conn: Connection = conn

    def insert_person(self, data: dict):
        try:
            person_id: str = self.uuid.smaller_uuid()
            data['person_id'] = person_id

            data_dict: dict = dict(PersonCreate(**data))
            data_list: list = list(data_dict.values())

            self.conn.cursor.execute(INSERT_PERSON, data_list)
            self.conn.connection.commit()
            self.conn.close()

            return True

        except Exception as e:
            raise e

    def select_person_by_email(self, email: str):
        try:
            self.conn.cursor.execute(SELECT_PERSON_BY_EMAIL, [email])
            person: tuple = self.conn.cursor.fetchone()
            return person

        except Exception:
            return None
