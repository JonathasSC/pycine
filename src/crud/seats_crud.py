from src.crud.base_crud import BaseCrud
from src.database.conn import Connection
from src.queries.seats_queries import (
    SELECT_SEATS_BY_ROOM_ID, SELECT_SEAT_BY_ID, SELECT_SEATS_BY_ROOM_ID_SEAT_CODE,
    UPDATE_SEAT_STATE)
from typing import Optional


class SeatsCrud(BaseCrud):
    def __init__(self, conn: Connection = None):
        super().__init__(conn)
        self.conn: Connection = Connection(auto_connect=False)

    def update_seat_state(self, seat_id, state):
        try:
            self.conn.connect()
            self.conn.cursor.execute(UPDATE_SEAT_STATE, [state, seat_id])
            self.conn.connection.commit()
            return seat_id

        except Exception as e:
            raise e

    def select_seats_by_room_id(self, room_id):
        try:
            self.conn.connect()
            self.conn.cursor.execute(SELECT_SEATS_BY_ROOM_ID, [room_id])
            seats_list: list = self.conn.cursor.fetchall()
            self.conn.close()

            return seats_list
        except Exception as e:
            raise e

    def select_seat_by_id(self, seat_id):
        try:
            self.conn.connect()
            self.conn.cursor.execute(SELECT_SEAT_BY_ID, [seat_id])
            seat: tuple = self.conn.cursor.fetchone()
            self.conn.close()

            return seat
        except Exception as e:
            raise e

    def select_seat_by_room_id_and_seat_code(self, room_id, seat_code) -> Optional[tuple]:
        try:
            self.conn.connect()
            self.conn.cursor.execute(
                SELECT_SEATS_BY_ROOM_ID_SEAT_CODE, [room_id, seat_code])
            seat: tuple = self.conn.cursor.fetchone()
            self.conn.close()
            return seat
        except Exception as e:
            raise e
