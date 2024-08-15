from typing import List, Dict, Any, Optional

from src.crud.base_crud import BaseCrud
from src.database.conn import Connection
from src.schemas.room_schemas import RoomCreate, RoomUpdate

from src.queries.rooms_queries import (
    INSERT_ROOM,
    UPDATE_ROOM,

    SELECT_ALL_ROOMS,
    SELECT_ROOM_BY_ID,
    SELECT_ROOM_BY_NAME,

    DELETE_ALL_ROOMS,
    DELETE_ROOM_BY_ID,
    DELETE_ROOM_BY_NAME,
)


class RoomsCrud(BaseCrud):
    def __init__(self, conn: Connection = None):
        super().__init__(conn)
        self.logger.info('INSTANCIA PERSONS CRUD CRIADA')

    def select_all_rooms(self) -> list:
        try:
            self.conn.connect()
            self.conn.cursor.execute(SELECT_ALL_ROOMS)
            room_list: list = self.conn.cursor.fetchall()
            self.conn.close()

            self.logger.info('SELECIONANDO TODAS AS SALAS')
            return room_list

        except Exception as e:
            raise e

    def select_room_by_name(self, room_name: str) -> Optional[tuple]:
        try:
            self.conn.connect()
            self.conn.cursor.execute(SELECT_ROOM_BY_NAME, [room_name])
            room: list = self.conn.cursor.fetchone()
            self.conn.close()

            self.logger.info('SELECIONANDO SALA POR NOME')
            return room
        except Exception as e:
            raise e

    def select_room_by_id(self, room_id: str) -> Optional[tuple]:
        try:
            self.conn.connect()
            self.conn.cursor.execute(SELECT_ROOM_BY_ID, [room_id])
            room: list = self.conn.cursor.fetchone()
            self.conn.close()

            self.logger.info('SELECIONANDO SALA POR ID')
            return room
        except Exception as e:
            raise e

    def insert_room(self, data: Dict[str, Any]) -> Optional[str]:
        try:
            room_id: str = self.uuid.smaller_uuid()
            data['room_id'] = room_id
            data_dict: Dict[str, Any] = dict(RoomCreate(**data))
            data_list: List[Any] = list(data_dict.values())

            self.conn.connect()
            self.conn.cursor.execute(INSERT_ROOM, data_list)
            self.conn.connection.commit()
            self.conn.close()

            self.logger.info('INSERINDO SALA')
            return room_id

        except Exception as e:
            raise e

    def update_room_by_id(self,
                          room_id: str,
                          data: Dict[str, Any]) -> Optional[str]:
        try:
            data_dict: Dict[str, Any] = dict(RoomUpdate(**data))

            data_list: List[str] = [
                data_dict.get('name', None),
                data_dict.get('rows', None),
                data_dict.get('columns', None),
                data_dict.get('type', None),
                room_id
            ]

            self.conn.connect()
            self.conn.cursor.execute(UPDATE_ROOM, data_list)
            self.conn.connection.commit()
            self.conn.close()

            self.logger.info('ATUALIZANDO SALA POR ID')
            return room_id

        except Exception as e:
            raise e

    def update_room_by_name(self,
                            room_name: str,
                            data: Dict[str, Any]) -> Optional[str]:
        try:
            data_dict: Dict[str, Any] = dict(RoomUpdate(**data))

            data_list: List[str] = [
                data_dict.get('name', None),
                data_dict.get('rows', None),
                data_dict.get('columns', None),
                data_dict.get('type', None),
                room_name
            ]

            self.conn.connect()
            self.conn.cursor.execute(UPDATE_ROOM, data_list)
            self.conn.connection.commit()
            self.conn.close()

            self.logger.info('ATUALIZANDO SALA POR EMAIL')
            return room_name

        except Exception as e:
            raise e

    def delete_all_rooms(self) -> Optional[bool]:
        try:
            self.conn.connect()
            self.conn.cursor.execute(DELETE_ALL_ROOMS)
            self.conn.connection.commit()
            self.conn.close()

            self.logger.info('DELETANDO TODAS AS SALAS')
            return True

        except Exception as e:
            raise e

    def delete_room_by_id(self, room_id: str) -> Optional[str]:

        try:
            if self.select_room_by_id(room_id):
                self.conn.connect()
                self.conn.cursor.execute(DELETE_ROOM_BY_ID, [room_id])
                self.conn.connection.commit()
                self.conn.close()

                self.logger.info('DELETANDO SALA POR ID')
                return room_id

            raise ValueError('Nenhuma sala com esse ID foi encontrado')

        except Exception as e:
            raise e

    def delete_room_by_name(self, room_name: str) -> Optional[str]:
        try:
            if self.select_room_by_id(room_name):
                self.conn.connect()
                self.conn.cursor.execute(DELETE_ROOM_BY_NAME, [room_name])
                self.conn.connection.commit()
                self.conn.close()

                self.logger.info('DELETANDO SALA POR NOME')
                return room_name

            raise ValueError('Nenhuma sala com esse NOME foi encontrado')

        except Exception as e:
            raise e
