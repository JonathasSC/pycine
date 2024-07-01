from src.crud.base_crud import BaseCrud
from src.database.conn import Connection


class SeatsCrud(BaseCrud):
    def __init__(self, conn: Connection = None):
        super().__init__(conn)
