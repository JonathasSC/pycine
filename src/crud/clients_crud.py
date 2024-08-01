from src.queries.clients_queries import (
    INSERT_CLIENT,
    DELETE_CLIENT,
    SELECT_ALL_CLIENTS,
    SELECT_CLIENT_BY_ID,
    UPDATE_PERSON_CLIENT_BY_CLIENT_ID
)
from typing import Any, Dict, List, Optional, Tuple
from src.crud.base_crud import BaseCrud
from src.database.conn import Connection
from src.schemas.client_schemas import ClientCreate


class ClientsCrud(BaseCrud):
    def __init__(self, conn: Connection = None):
        super().__init__(conn)
        self.logger.info('INSTANCIA CLIENTS CRUD CRIADA')

    def insert_client(self, person_id: str) -> Optional[str]:
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

            self.logger.info('INSERINDO CLIENTE')
            return client_id

        except Exception as e:
            return e

    def select_all_clients(self) -> Optional[List[Tuple[str]]]:
        try:
            self.conn.connect()
            self.conn.cursor.execute(SELECT_ALL_CLIENTS)
            client_list: list = self.conn.cursor.fetchall()
            self.conn.close()

            self.logger.info('SELECIONANDO TODOS OS CLIENTES')
            return client_list

        except Exception as e:
            return e

    def delete_client(self, client_id):
        try:
            self.conn.connect()
            self.conn.cursor.execute(DELETE_CLIENT, [client_id])
            self.conn.connection.commit()
            self.conn.close()

            self.logger.info('DELETANDO CLIENTE POR ID')
            return client_id

        except Exception as e:
            return e

    def update_client(self, client_id: str, data: dict) -> Optional[Tuple[str]]:
        try:
            data_list: List[str] = [
                data.get('name', None),
                data.get('email', None),
                data.get('password', None),
                client_id
            ]

            self.conn.connect()
            self.conn.cursor.execute(
                UPDATE_PERSON_CLIENT_BY_CLIENT_ID,
                data_list
            )

            self.conn.connection.commit()
            self.conn.cursor.execute(
                SELECT_CLIENT_BY_ID(client_id)
            )

            client: tuple = self.conn.cursor.fetchone()
            self.conn.close()

            self.logger.info('ATUALIZANDO CLIENT POR ID')
            return client

        except Exception as e:
            raise e

    def select_by_id(self, client_id: str) -> tuple:
        try:
            self.conn.connect()
            self.conn.cursor.execute(SELECT_CLIENT_BY_ID, [client_id])
            client: tuple = self.conn.cursor.fetchone()
            self.conn.close()

            self.logger.info('SELECIONANDO CLIENTE POR ID')
            return client

        except Exception as e:
            raise e
