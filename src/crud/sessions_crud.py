from typing import List, Dict, Any

from src.crud.base_crud import BaseCrud
from src.database.conn import Connection
from src.schemas.session_schemas import SessionCreate

from src.queries.sessions_queries import (
    SELECT_ALL_SESSIONS,
    INSERT_SESSION,
    UPDATE_SESSION,
    DELETE_SESSION
)


class SessionsCrud(BaseCrud):
    def __init__(self, conn: Connection = None):
        super().__init__(conn)

    def select_all_sessions(self) -> List[Dict[str, Any]]:
        try:
            self.conn.cursor.execute(SELECT_ALL_SESSIONS)
            session_list: List[Dict[str, Any]] = self.conn.cursor.fetchall()
            return session_list
        except Exception as e:
            raise e

    def insert_session(self, data: Dict[str, Any]) -> bool:
        try:
            session_id: str = self.uuid.smaller_uuid()
            data['session_id'] = session_id
            session_data: Dict[str, Any] = dict(SessionCreate(**data))
            data_list: List[Any] = list(session_data.values())

            self.conn.cursor.execute(INSERT_SESSION, data_list)
            self.conn.connection.commit()
            return True

        except Exception as e:
            raise e

    def update_session(self, data: Dict[str, Any]) -> bool:
        try:
            session_data: Dict[str, Any] = dict(SessionCreate(**data))
            data_list: List[Any] = list(session_data.values())
            self.conn.cursor.execute(UPDATE_SESSION, data_list)
            self.conn.connection.commit()
            return True

        except Exception as e:
            raise e

    def delete_session(self, session_id: str) -> bool:
        try:
            self.conn.cursor.execute(DELETE_SESSION, (session_id,))
            self.conn.connection.commit()
            return True

        except Exception as e:
            raise e
