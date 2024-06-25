from src.queries.admins_queries import INSERT_ADMIN, SELECT_COUNT_ADMINS
from src.crud.base_crud import BaseCrud
from src.database.conn import Connection


class AdminsCrud(BaseCrud):
    def __init__(self, conn: Connection = None):
        super().__init__(conn)

    def insert_admin(self, person_id: str) -> None:
        admin_id: str = self.uuid.smaller_uuid()
        self.conn.cursor.execute(INSERT_ADMIN, [admin_id, person_id])
        self.conn.connection.commit()

    def get_count_admin(self) -> int:
        try:
            self.conn.cursor.execute(SELECT_COUNT_ADMINS)
            count_admin: int = self.conn.cursor.fetchone()[0]
            return count_admin

        except Exception as e:
            return e
