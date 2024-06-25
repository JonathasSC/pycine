from src.crud.base_crud import BaseCrud
from src.queries.movies_queries import SELECT_ALL_MOVIES, INSERT_MOVIE
from src.database.conn import Connection
from src.schemas.movie_schemas import MovieCreate
from typing import List, Dict, Any


class MoviesCrud(BaseCrud):
    def __init__(self, conn: Connection = None):
        super().__init__(conn)

    def select_all_movies(self) -> list:
        try:
            self.conn.cursor.execute(SELECT_ALL_MOVIES)
            movies_list: list = self.conn.cursor.fetchall()
            return movies_list
        except Exception as e:
            raise e

    def insert_movie(self, data: Dict[str, Any]):
        try:
            movie_id: str = self.uuid.smaller_uuid()
            data['movie_id'] = movie_id
            data_dict: Dict[str, Any] = dict(MovieCreate(**data))
            data_list: List[Any] = list(data_dict.values())

            self.conn.cursor.execute(INSERT_MOVIE, data_list)
            self.conn.connection.commit()
            return True

        except Exception as e:
            raise e
