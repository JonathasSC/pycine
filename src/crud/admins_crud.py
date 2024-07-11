from src.queries.admins_queries import (
    INSERT_ADMIN,
    DELETE_ADMIN,
    SELECT_COUNT_ADMINS,
    SELECT_ADMIN_IN_PERSON,
)
from src.crud.base_crud import BaseCrud
from src.database.conn import Connection
from src.schemas.admin_schemas import AdminCreate

from typing import Any, Dict, List


class AdminsCrud(BaseCrud):
    def __init__(self, conn: Connection = None):
        super().__init__(conn)
        self.conn: Connection = Connection(auto_connect=False)

    def insert_admin(self, person_id: str) -> None:
        try:
            data: dict = {}
            admin_id: str = self.uuid.smaller_uuid()

            data['admin_id'] = admin_id
            data['person_id'] = person_id

            data_dict: Dict[str, Any] = dict(AdminCreate(**data))
            data_list: List[Any] = list(data_dict.values())

            self.conn.connect()
            self.conn.cursor.execute(INSERT_ADMIN, data_list)
            self.conn.connection.commit()
            self.conn.close()

            self.logger.info('ADMIN INSERIDO NO BANCO DE DADOS')
            return admin_id

        except Exception as e:
            raise e

    def delete_admin(self, admin_id: str) -> bool:
        try:
            self.conn.connect()
            self.conn.cursor.execute(DELETE_ADMIN, [admin_id])
            self.conn.connection.commit()
            self.conn.close()

        except Exception as e:
            self.logger.warning('EXCESSÃO TENTAR DELETAR ADMIN')
            raise e

        self.logger.info('ADMIN DELETADO')
        return True

    def select_all_admins(self) -> list:
        try:
            self.conn.connect()
            self.conn.cursor.execute(SELECT_ADMIN_IN_PERSON)
            admin_list: list = self.conn.cursor.fetchall()
            self.conn.close()

        except Exception as e:
            self.logger.warning('EXCESSÃO TENTAR LISTAR ADMIN')
            raise e

        self.logger.info('ADMINS LISTADOS')
        return admin_list

    def get_count_admin(self) -> int:
        try:
            self.logger.info('TENTANDO CONTAR QUANTIDADE DE ADMINS')

            self.conn.connect()
            self.conn.cursor.execute(SELECT_COUNT_ADMINS)
            count_admin: int = self.conn.cursor.fetchone()[0]
            self.conn.close()

        except Exception as e:
            self.logger.warning('EXCESSÃO TENTAR MOSTRAR QUANTIDADE DE ADMINS')
            raise e

        self.logger.info('QUANTIDADE DA ADMINS CONTADA BEM SUCEDIDO')
        return count_admin
