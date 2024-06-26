from typing import List, Dict, Any, Optional

from src.crud.base_crud import BaseCrud
from src.database.conn import Connection
from src.schemas.session_schemas import SessionCreate

from src.queries.sessions_queries import (
    SELECT_SESSIONS_BY_MOVIE_ID,
    SELECT_ALL_SESSIONS,
    INSERT_SESSION,
    UPDATE_SESSION,
    DELETE_SESSION,
    SELECT_SESSIONS_WITH_ROOM_DETAILS,
    SELECT_ALL_SESSIONS_WITH_MOVIES,
    DELETE_ALL_SESSIONS,
)


class SessionsCrud(BaseCrud):
    def __init__(self, conn: Connection = None):
        super().__init__(conn)

    def select_session_by_movie_id(self, movie_id) -> Optional[tuple]:
        try:
            self.conn.cursor.execute(SELECT_SESSIONS_BY_MOVIE_ID, [movie_id])
            session_list: List[Dict[str, Any]] = self.conn.cursor.fetchall()
            return session_list
        except Exception as e:
            raise e

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

    def select_sessions_with_room_details(self, movie_id: str) -> List[Dict[str, Any]]:
        try:
            self.conn.cursor.execute(
                SELECT_SESSIONS_WITH_ROOM_DETAILS,
                [movie_id]
            )
            session_list: List[Dict[str, Any]] = self.conn.cursor.fetchall()
            return session_list

        except Exception as e:
            raise e

    def select_all_session_with_movies(self):
        try:
            self.conn.cursor.execute(SELECT_ALL_SESSIONS_WITH_MOVIES)
            session_list: List[Dict[str, Any]] = self.conn.cursor.fetchall()
            return session_list

        except Exception as e:
            raise e

    def delete_all_sessions(self):
        try:
            self.conn.cursor.execute(DELETE_ALL_SESSIONS)
            self.conn.connection.commit()
            return True

        except Exception as e:
            raise e
