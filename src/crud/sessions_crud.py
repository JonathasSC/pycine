from datetime import datetime

from src.crud.base_crud import BaseCrud
from src.database.conn import Connection
from typing import List, Dict, Any, Optional, Tuple
from src.schemas.session_schemas import SessionCreate, SessionUpdate

from src.queries.sessions_queries import (
    INSERT_SESSION,
    UPDATE_SESSION,
    DELETE_SESSION,
    SELECT_ALL_SESSIONS,
    DELETE_ALL_SESSIONS,
    SELECT_SESSIONS_BY_ID,
    SELECT_SESSIONS_BY_MOVIE_ID,
    SELECT_ALL_SESSIONS_WITH_MOVIES,
    SELECT_SESSIONS_BY_MOVIE_ID_WITH_ROOM_DETAILS,
)


class SessionsCrud(BaseCrud):
    def __init__(self, conn: Connection = None):
        super().__init__(conn)
        self.logger.info('INSTANCIA SESSIONS CRUD CRIADA')

    def select_session_by_id(self, session_id):
        try:
            self.conn.connect()
            self.conn.cursor.execute(SELECT_SESSIONS_BY_ID, [session_id])
            session_list: tuple = self.conn.cursor.fetchone()
            self.conn.close()

            self.logger.info('SELECIONANDO SESSÃO')
            return session_list
        except Exception as e:
            raise e

    def select_sessions_by_movie_id(self, movie_id) -> Optional[List[Tuple[str]]]:
        try:
            self.conn.connect()
            self.conn.cursor.execute(SELECT_SESSIONS_BY_MOVIE_ID, [movie_id])
            session_list: List[Dict[str, Any]] = self.conn.cursor.fetchall()
            self.conn.close()

            self.logger.info('SELECIONANDO TODAS AS SESSÕES POR MOVIE ID')
            return session_list
        except Exception as e:
            raise e

    def select_all_sessions(self) -> Optional[List[Tuple[str]]]:
        try:
            self.conn.connect()
            self.conn.cursor.execute(SELECT_ALL_SESSIONS)
            session_list: List[Dict[str, Any]] = self.conn.cursor.fetchall()
            self.conn.close()

            self.logger.info('SELECIONANDO TODAS AS SESSÕES')
            return session_list

        except Exception as e:
            raise e

    def insert_session(self, data: Dict[str, Any]) -> Optional[str]:
        try:
            session_id: str = self.uuid.smaller_uuid()
            data['session_id'] = session_id

            session_dict: Dict[str, Any] = dict(SessionCreate(**data))

            now = datetime.now()
            start_date = session_dict.get('start_date', None)
            start_time = session_dict.get('start_time', None)

            if start_date and start_time:
                session_datetime = datetime.combine(start_date, start_time)
                if session_datetime < now:
                    raise ValueError(
                        'A sessão não pode ser agendada para uma data e hora no passado.')

            data_list: List[any] = [
                session_dict.get('session_id', None),
                session_dict.get('room_id', None),
                session_dict.get('movie_id', None),

                str(session_dict.get('price', None)),

                session_dict.get('start_date', None).isoformat(),
                session_dict.get('start_time', None).strftime('%H:%M')
            ]

            self.conn.connect()
            self.conn.cursor.execute(INSERT_SESSION, data_list)
            self.conn.connection.commit()
            self.conn.close()

            self.logger.info('INSERINDO SESSÃO')
            return session_id

        except Exception as e:
            raise e

    def update_session(self, session_id: str, session_data: Dict[str, Any]) -> Optional[str]:
        try:
            data_dict: Dict[str, Any] = dict(SessionUpdate(**session_data))

            data_list: List[any] = [
                data_dict.get('room_id', None),
                data_dict.get('movie_id', None),
                data_dict.get('price', None),
                data_dict.get('start_time', None),
                session_id
            ]

            self.conn.connect()
            self.conn.cursor.execute(UPDATE_SESSION, data_list)
            self.conn.connection.commit()
            self.conn.close()

            self.logger.info('ATUALIZANDO SESSÃO')
            return session_id

        except Exception as e:
            raise e

    def delete_session(self, session_id: str) -> Optional[str]:
        try:
            self.conn.connect()
            self.conn.cursor.execute(DELETE_SESSION, (session_id,))
            self.conn.connection.commit()
            self.conn.close()

            self.logger.info('DELETANDO SESSÃO')
            return session_id

        except Exception as e:
            raise e

    def select_sessions_by_movie_id_with_room_details(self, movie_id: str) -> Optional[List[Tuple[str]]]:
        try:
            self.conn.connect()
            self.conn.cursor.execute(
                SELECT_SESSIONS_BY_MOVIE_ID_WITH_ROOM_DETAILS,
                [movie_id]
            )

            session_list: List[Dict[str, Any]] = self.conn.cursor.fetchall()
            self.conn.close()

            self.logger.info('SELECIONADO SESSÃO PELO ID COM DETALHES DA SALA')
            return session_list

        except Exception as e:
            raise e

    def select_all_session_with_movies(self) -> Optional[List[Tuple[str]]]:
        try:
            self.conn.connect()
            self.conn.cursor.execute(SELECT_ALL_SESSIONS_WITH_MOVIES)
            session_list: List[Dict[str, Any]] = self.conn.cursor.fetchall()
            self.conn.close()

            self.logger.info('SELECIONADO LISTA DE SESSÕES')
            return session_list

        except Exception as e:
            raise e

    def delete_all_sessions(self) -> Optional[bool]:
        try:
            self.conn.connect()
            self.conn.cursor.execute(DELETE_ALL_SESSIONS)
            self.conn.connection.commit()
            self.conn.close()
            self.logger.info('DELETANDO TODAS AS SESSÕES')

            return True

        except Exception as e:
            raise e
