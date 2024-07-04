from src.crud.base_crud import BaseCrud
from src.queries.movies_queries import SELECT_ALL_MOVIES, INSERT_MOVIE, DELETE_ALL_MOVIES, SELECT_MOVIE_BY_ID
from src.database.conn import Connection
from src.schemas.movie_schemas import MovieCreate
from typing import List, Dict, Any


class MoviesCrud(BaseCrud):
    def __init__(self, conn: Connection = None):
        super().__init__(conn)
        self.conn: Connection = Connection(auto_connect=False)

    def select_movie_by_id(self, movie_id) -> tuple:
        try:
            self.conn.connect()
            self.conn.cursor.execute(SELECT_MOVIE_BY_ID, [movie_id])
            movie: tuple = self.conn.cursor.fetchone()
            self.conn.close()

            self.logger.info('SELECIONANDO FILME POR ID')
            return movie

        except Exception as e:
            raise e

    def select_all_movies(self) -> list:
        try:
            self.conn.connect()
            self.conn.cursor.execute(SELECT_ALL_MOVIES)
            movies_list: list = self.conn.cursor.fetchall()
            self.conn.close()

            self.logger.info('SELECIONANDO TODOS OS FILMES')
            return movies_list
        except Exception as e:
            raise e

    def insert_movie(self, data: Dict[str, Any]):
        try:
            movie_id: str = self.uuid.smaller_uuid()
            data['movie_id'] = movie_id
            data_dict: Dict[str, Any] = dict(MovieCreate(**data))
            data_list: List[Any] = list(data_dict.values())

            self.conn.connect()
            self.conn.cursor.execute(INSERT_MOVIE, data_list)
            self.conn.connection.commit()
            self.conn.close()

            return movie_id

        except Exception as e:
            raise e

    def delete_all_movies(self):
        try:
            self.conn.cursor.execute(DELETE_ALL_MOVIES)
            self.conn.connection.commit()
            return True

        except Exception as e:
            raise e
