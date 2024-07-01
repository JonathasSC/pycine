from src.utils.uuid import UUID
from src.queries.clients_queries import INSERT_CLIENT
from src.crud.base_crud import BaseCrud
from src.database.conn import Connection
from typing import Any, Dict, List
from src.schemas.client_schemas import ClientCreate


class ClientsCrud(BaseCrud):
    def __init__(self, conn: Connection = None):
        super().__init__(conn)

    def insert_client(self, person_id: str) -> bool:
        try:
            data: dict = {}
            client_id: str = self.uuid.smaller_uuid()
            data['client_id'] = client_id
            data['person_id'] = person_id

            data_dict: Dict[str, Any] = dict(ClientCreate(**data))
            data_list: List[Any] = list(data_dict.values())

            self.conn.cursor.execute(INSERT_CLIENT, data_list)
            self.conn.connection.commit()
            return client_id

        except Exception as e:
            return e
