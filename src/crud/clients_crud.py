from src.queries.clients_queries import (
    INSERT_CLIENT,
    SELECT_ALL_CLIENTS,
    DELETE_CLIENT
)
from typing import Any, Dict, List
from src.crud.base_crud import BaseCrud
from src.database.conn import Connection
from src.schemas.client_schemas import ClientCreate


class ClientsCrud(BaseCrud):
    def __init__(self, conn: Connection = None):
        super().__init__(conn)
        self.conn: Connection = Connection(auto_connect=False)

    def insert_client(self, person_id: str) -> bool:
        try:
            data: dict = {}
            client_id: str = self.uuid.smaller_uuid()
            data['client_id'] = client_id
            data['person_id'] = person_id

            data_dict: Dict[str, Any] = dict(ClientCreate(**data))
            data_list: List[Any] = list(data_dict.values())

            self.conn.connect()
            self.conn.cursor.execute(INSERT_CLIENT, data_list)
            self.conn.connection.commit()
            self.conn.close()

            return client_id

        except Exception as e:
            return e

    def select_all_clients(self):
        try:
            self.conn.connect()
            self.conn.cursor.execute(SELECT_ALL_CLIENTS)
            client_list: list = self.conn.cursor.fetchall()
            self.conn.close()
            return client_list

        except Exception as e:
            return e

    def delete_client(self, client_id):
        try:
            self.conn.connect()
            self.conn.cursor.execute(DELETE_CLIENT, [client_id])
            self.conn.connection.commit()
            return client_id

        except Exception as e:
            return e
