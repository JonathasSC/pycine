from src.crud.base_crud import BaseCrud
from src.database.conn import Connection
from src.queries.seats_queries import SELECT_SEATS_BY_ROOM_ID
from time import sleep


class SeatsCrud(BaseCrud):
    def __init__(self, conn: Connection = None):
        super().__init__(conn)

    def get_seats_by_room_id(self, room_id):
        try:
            self.conn.cursor.execute(SELECT_SEATS_BY_ROOM_ID, [room_id])
            seats_list: list = self.conn.cursor.fetchall()
            return seats_list
        except Exception as e:
            raise e
