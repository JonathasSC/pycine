from typing import List, Dict, Any, Optional

from src.crud.base_crud import BaseCrud
from src.database.conn import Connection
from src.schemas.room_schemas import RoomCreate, RoomUpdate


from src.queries.rooms_queries import (
    SELECT_ALL_ROOMS,
    INSERT_ROOM,
    UPDATE_ROOM,
    DELETE_ALL_ROOMS,
    SELECT_ROOM_BY_ID,
)

from src.queries.seats_queries import INSERT_SEAT


class RoomsCrud(BaseCrud):
    def __init__(self, conn: Connection = None):
        super().__init__(conn)

    def select_all_rooms(self) -> list:
        try:
            self.conn.cursor.execute(SELECT_ALL_ROOMS)
            room_list: list = self.conn.cursor.fetchall()
            return room_list
        except Exception as e:
            raise e

    def select_by_room_id(self, room_id) -> Optional[tuple]:
        try:
            self.conn.cursor.execute(SELECT_ROOM_BY_ID, [room_id])
            room: list = self.conn.cursor.fetchone()
            return room
        except Exception as e:
            raise e

    def insert_room_with_seats(self, data: Dict[str, Any]) -> Optional[str]:
        try:
            room_id: str = self.uuid.smaller_uuid()
            data['room_id'] = room_id
            data_dict: Dict[str, Any] = dict(RoomCreate(**data))
            data_list: List[Any] = list(data_dict.values())

            self.conn.connect()
            self.conn.cursor.execute(INSERT_ROOM, data_list)

            rows = data['rows']
            columns = data['columns']

            for row in range(1, rows + 1):
                row_letter = chr(64 + row)
                for col in range(1, columns + 1):
                    seat_code = f"{row_letter}{col}"
                    seat_id = self.uuid.smaller_uuid()
                    seat_state = 'available'
                    self.conn.cursor.execute(
                        INSERT_SEAT,
                        (seat_id, room_id, seat_code, row, col, seat_state)
                    )

            self.conn.connection.commit()
            self.conn.close()

            return room_id

        except Exception as e:
            self.conn.connection.rollback()
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

            return room_id

        except Exception as e:
            raise e

    def update_room(self,
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

            return room_id

        except Exception as e:
            raise e

    def delete_all_rooms(self) -> Optional[bool]:
        try:
            self.conn.cursor.execute(DELETE_ALL_ROOMS)
            self.conn.connection.commit()
            return True

        except Exception as e:
            raise e
