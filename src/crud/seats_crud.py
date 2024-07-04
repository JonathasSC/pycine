from src.crud.base_crud import BaseCrud
from src.database.conn import Connection
from src.queries.seats_queries import SELECT_SEATS_BY_ROOM_ID, SELECT_SEAT_BY_ID
from time import sleep


class SeatsCrud(BaseCrud):
    def __init__(self, conn: Connection = None):
        super().__init__(conn)
        self.conn: Connection = Connection(auto_connect=False)

    def get_seats_by_room_id(self, room_id):
        try:
            self.conn.connect()
            self.conn.cursor.execute(SELECT_SEATS_BY_ROOM_ID, [room_id])
            seats_list: list = self.conn.cursor.fetchall()
            self.conn.close()

            return seats_list
        except Exception as e:
            raise e

    def get_seat_by_id(self, seat_id):
        try:
            self.conn.connect()
            self.conn.cursor.execute(SELECT_SEAT_BY_ID, [seat_id])
            seats_list: list = self.conn.cursor.fetchone()
            self.conn.close()

            return seats_list
        except Exception as e:
            raise e
