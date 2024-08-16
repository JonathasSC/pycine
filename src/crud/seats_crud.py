from src.crud.base_crud import BaseCrud
from src.database.conn import Connection
from src.queries.seats_queries import (
    INSERT_SEAT,
    SELECT_SEAT_BY_ID,
    UPDATE_SEAT_STATE,
    SELECT_SEATS_BY_ROOM_ID,
    DELETE_SEATS_BY_ROOM_NAME,
    SELECT_SEATS_BY_ROOM_NAME,
    SELECT_COUNT_SEATS_BY_ROOM_ID,
    SELECT_SEATS_BY_ROOM_ID_SEAT_CODE,
    SELECT_SEATS_BY_ROOM_NAME_SEAT_CODE,
)

from typing import Optional, Dict, List, Any
from src.schemas.seat_schemas import SeatCreate


class SeatsCrud(BaseCrud):
    def __init__(self, conn: Connection = None):
        super().__init__(conn)
        self.logger.info('INSTANCIA SEATS CRUD CRIADA')

# COUNT SEATS
    def count_seats_by_room_id(self, room_id: str):
        try:
            self.conn.connect()
            self.conn.cursor.execute(SELECT_COUNT_SEATS_BY_ROOM_ID, [room_id])
            seats_count: int = self.conn.cursor.fetchone()[0]
            self.logger.info(
                'PESQUISANDO QUANTIDADES DE ASSENTOS POR ID DE SALA')
            return seats_count
        except Exception as e:
            raise e

# DELETE
    def delete_seats_by_room_name(self, room_name: str) -> Optional[str]:
        try:
            if self.select_seats_by_room_name(room_name):
                self.conn.connect()
                self.conn.cursor.execute(
                    DELETE_SEATS_BY_ROOM_NAME, [room_name])
                self.conn.connection.commit()
                self.conn.close()
                return True
            return False

        except Exception as e:
            raise e

# UPDATE
    def update_seat_state(self, seat_id: str, state: str) -> Optional[str]:
        try:
            self.conn.connect()
            self.conn.cursor.execute(UPDATE_SEAT_STATE, [state, seat_id])
            self.conn.connection.commit()
            return seat_id

        except Exception as e:
            raise e

# INSERTS
    def insert_seat(self, data: dict) -> Optional[str]:
        try:
            seat_id: str = self.uuid.smaller_uuid()
            data['seat_id'] = seat_id

            seat_dict: Dict[str, Any] = dict(SeatCreate(**data))

            data_list: List[any] = [
                seat_dict.get('seat_id', None),
                seat_dict.get('room_id', None),
                seat_dict.get('seat_code', None),
                seat_dict.get('row', None),
                seat_dict.get('col', None),
                seat_dict.get('state', None),
            ]

            self.conn.connect()
            self.conn.cursor.execute(INSERT_SEAT, data_list)
            self.conn.connection.commit()
            self.conn.close()

            return seat_id

        except Exception as e:
            raise e

    def insert_seats_by_room(self, room: tuple):
        try:
            room_id = room[0]
            rows = room[2]
            columns = room[3]

            for row in range(1, rows + 1):
                row_letter = chr(64 + row)
                for col in range(1, columns + 1):
                    seat_data: dict = {}

                    seat_data['room_id'] = room_id
                    seat_data['seat_code'] = f"{row_letter}{col}"
                    seat_data['row'] = row
                    seat_data['col'] = col
                    seat_data['state'] = 'available'

                    self.insert_seat(seat_data)

        except Exception as e:
            raise e

# SELECTS
    def select_seats_by_room_name(self, room_name: str) -> Optional[str]:
        try:
            self.conn.connect()
            self.conn.cursor.execute(
                SELECT_SEATS_BY_ROOM_NAME, [room_name])
            seats_list: list = self.conn.cursor.fetchall()
            self.conn.close()

            return seats_list
        except Exception as e:
            raise e

    def select_seats_by_room_id(self, room_id: str) -> Optional[list]:
        try:
            self.conn.connect()
            self.conn.cursor.execute(SELECT_SEATS_BY_ROOM_ID, [room_id])
            seats_list: list = self.conn.cursor.fetchall()
            self.conn.close()

            return seats_list
        except Exception as e:
            raise e

    def select_seat_by_id(self, seat_id: str) -> Optional[tuple]:
        try:
            self.conn.connect()
            self.conn.cursor.execute(SELECT_SEAT_BY_ID, [seat_id])
            seat: tuple = self.conn.cursor.fetchone()
            self.conn.close()

            return seat
        except Exception as e:
            raise e

    def select_seat_by_room_id_and_seat_code(self, room_id: str, seat_code: str) -> Optional[tuple]:
        try:
            self.conn.connect()
            self.conn.cursor.execute(
                SELECT_SEATS_BY_ROOM_ID_SEAT_CODE, [room_id, seat_code])
            seat: tuple = self.conn.cursor.fetchone()
            self.conn.close()

            return seat
        except Exception as e:
            raise e

    def select_seat_by_room_name_and_seat_code(self, room_name: str, seat_code: str) -> Optional[tuple]:
        try:
            self.conn.connect()
            self.conn.cursor.execute(
                SELECT_SEATS_BY_ROOM_NAME_SEAT_CODE, [room_name, seat_code])
            seat: tuple = self.conn.cursor.fetchone()
            self.conn.close()

            return seat
        except Exception as e:
            raise e
