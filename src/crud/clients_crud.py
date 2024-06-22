from src.utils.uuid import UUID
from src.database.conn import Connection
from src.queries.clients_queries import INSERT_CLIENT


class ClientsCrud:
    def __init__(self, conn: Connection = Connection()):
        self.conn = conn
        self.uuid: UUID = UUID()

    def insert_client(self, person_id: str):
        try:
            client_id: str = self.uuid.smaller_uuid()
            self.conn.cursor.execute(INSERT_CLIENT, [client_id, person_id])
            self.conn.connection.commit()
            self.conn.close()
            return True

        except Exception as e:
            return e
