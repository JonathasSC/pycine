from src.queries.admins_queries import SELECT_COUNT_ADMINS, INSERT_ADMIN
from src.crud.base_crud import BaseCrud
from src.database.conn import Connection
from src.schemas.admin_schemas import AdminCreate
from typing import Any, Dict, List


class AdminsCrud(BaseCrud):
    def __init__(self, conn: Connection = None):
        super().__init__(conn)

    def insert_admin(self, person_id: str) -> None:
        data: dict = {}
        data['admin_id'] = self.uuid.smaller_uuid()
        data['person_id'] = person_id

        data_dict: Dict[str, Any] = dict(AdminCreate(**data))
        data_list: List[Any] = list(data_dict.values())

        self.conn.cursor.execute(INSERT_ADMIN, data_list)
        self.conn.connection.commit()
        return True

    def get_count_admin(self) -> int:
        try:
            self.conn.cursor.execute(SELECT_COUNT_ADMINS)
            count_admin: int = self.conn.cursor.fetchone()[0]
            return count_admin

        except Exception as e:
            return e
