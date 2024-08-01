from src.queries.admins_queries import (
    INSERT_ADMIN,
    DELETE_ADMIN,
    SELECT_ADMIN_BY_ID,
    SELECT_COUNT_ADMINS,
    SELECT_ADMIN_IN_PERSON,
    UPDATE_PERSON_ADMIN_BY_ADMIN_ID,
    DELETE_ALL_ADMINS,
)
from src.queries.persons_queries import (
    DELETE_PERSON_BY_ID,
    SELECT_PERSON_BY_ID
)

from src.crud.base_crud import BaseCrud
from src.database.conn import Connection

from src.schemas.admin_schemas import AdminCreate
from typing import Any, Dict, List, Optional


class AdminsCrud(BaseCrud):
    def __init__(self, conn: Connection = None):
        super().__init__(conn)
        self.logger.info('INSTANCIA ADMIN CRUD CRIADA')

    def select_by_id(self, admin_id: str) -> tuple:
        try:
            self.conn.connect()
            self.conn.cursor.execute(SELECT_ADMIN_BY_ID, [admin_id])
            admin: tuple = self.conn.cursor.fetchone()
            return admin

        except Exception as e:
            raise e

    def insert_admin(self, person_id: str) -> str:
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

    def delete_admin(self, admin_id: str) -> Optional[str]:
        try:
            self.conn.connect()
            self.conn.cursor.execute(SELECT_ADMIN_BY_ID, [admin_id])
            admin: tuple = self.conn.cursor.fetchone()

            self.conn.cursor.execute(SELECT_PERSON_BY_ID, [admin[1]])
            person: tuple = self.conn.cursor.fetchone()
            person_id: str = person[0]

            self.conn.cursor.execute(DELETE_ADMIN, [admin_id])
            self.conn.cursor.execute(DELETE_PERSON_BY_ID, [person_id])

            self.conn.connection.commit()
            self.conn.close()
            self.logger.info('ADMIN E PESSOA ASSOCIADA DELETADOS')
            return admin_id

        except Exception as e:
            self.logger.warning('EXCEÇÃO AO TENTAR DELETAR ADMIN')
            raise e

    def select_all_admins(self) -> list:
        try:
            self.conn.connect()
            self.conn.cursor.execute(SELECT_ADMIN_IN_PERSON)
            admin_list: list = self.conn.cursor.fetchall()
            self.conn.close()

            self.logger.info('ADMINS LISTADOS')
            return admin_list

        except Exception as e:
            self.logger.warning('EXCESSÃO TENTAR LISTAR ADMIN')
            raise e

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

    def update_admin(self, admin_id: str, data: dict) -> None:
        try:
            self.logger.info(
                'TENTANDO ATUALIZAR DADOS DE PERSONS QUE SÃO ADMINS BASEADO NO admin_id')

            data_list: List[str] = [
                data.get('name', None),
                data.get('email', None),
                data.get('password', None),
                admin_id
            ]

            self.conn.connect()
            self.conn.cursor.execute(
                UPDATE_PERSON_ADMIN_BY_ADMIN_ID,
                data_list
            )

            self.conn.connection.commit()
            self.conn.close()

            self.logger.info(
                'DADOS DE PERSONS QUE SÃO ADMINS ATUALIZADOS NO BANCO DE DADOS')

        except Exception as e:
            self.logger.warning(
                'EXCEÇÃO AO TENTAR ATUALIZAR DADOS DE PERSONS QUE SÃO ADMINS')
            raise e

    def delete_all_admins(self) -> None:
        self.conn.connect()
        self.conn.cursor.execute(DELETE_ALL_ADMINS)
        self.conn.connection.commit()
        self.conn.close()
