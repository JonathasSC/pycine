from src.crud.base_crud import BaseCrud
from src.queries.movies_queries import (
    SELECT_ALL_MOVIES,
    INSERT_MOVIE,
    DELETE_ALL_MOVIES,
    SELECT_MOVIE_BY_ID,
    SELECT_MOVIE_BY_NAME,
    DELETE_MOVIE,
    UPDATE_MOVIE
)
from src.database.conn import Connection
from typing import List, Dict, Any, Optional
from src.schemas.movie_schemas import MovieCreate, MovieUpdate


class MoviesCrud(BaseCrud):
    def __init__(self, conn: Connection = None):
        super().__init__(conn)
        self.logger.info('INSTANCIA MOVIES CRUD CRIADA')

    def select_movie_by_id(self, movie_id) -> Optional[tuple]:
        try:
            self.conn.connect()
            self.conn.cursor.execute(SELECT_MOVIE_BY_ID, [movie_id])
            movie: tuple = self.conn.cursor.fetchone()
            self.conn.close()

            self.logger.info('SELECIONANDO FILME POR ID')
            return movie

        except Exception as e:
            raise e

    def select_movie_by_name(self, movie_name) -> Optional[tuple]:
        try:
            self.conn.connect()
            self.conn.cursor.execute(SELECT_MOVIE_BY_NAME, [movie_name])
            movie: tuple = self.conn.cursor.fetchone()
            self.conn.close()

            self.logger.info('INSERINDO FILME POR NOME')
            return movie
        except Exception as e:
            raise e

    def select_all_movies(self) -> Optional[list]:
        try:
            self.conn.connect()
            self.conn.cursor.execute(SELECT_ALL_MOVIES)
            movies_list: list = self.conn.cursor.fetchall()
            self.conn.close()

            self.logger.info('SELECIONANDO TODOS OS FILMES')
            return movies_list
        except Exception as e:
            raise e

    def insert_movie(self, data: Dict[str, Any]) -> Optional[str]:
        try:
            movie_id: str = self.uuid.smaller_uuid()
            data['movie_id'] = movie_id
            data_dict: Dict[str, Any] = dict(MovieCreate(**data))
            data_list: List[Any] = list(data_dict.values())

            self.conn.connect()
            self.conn.cursor.execute(INSERT_MOVIE, data_list)
            self.conn.connection.commit()
            self.conn.close()

            self.logger.info('INSERINDO FILME')
            return movie_id

        except Exception as e:
            raise e

    def delete_all_movies(self) -> Optional[bool]:
        try:
            self.conn.connect()
            self.conn.cursor.execute(DELETE_ALL_MOVIES)
            self.conn.connection.commit()
            self.conn.close()

            self.logger.info('DELETANDO TODOS OS FILMES')
            return True

        except Exception as e:
            raise e

    def delete_movie(self, movie_id: str) -> Optional[str]:
        try:
            if self.select_movie_by_id(movie_id):
                self.conn.connect()
                self.conn.cursor.execute(DELETE_MOVIE, [movie_id])
                self.conn.connection.commit()
                self.conn.close()

                self.logger.info('DELETANDO FILME POR ID')
                return movie_id
            raise ValueError('Nenhum filme com esse ID foi encontrado')

        except Exception as e:
            raise e

    def update_movie(self, movie_id: str, data: Dict[str, str]) -> Optional[str]:
        try:
            data_dict: Dict[str, Any] = dict(MovieUpdate(**data))

            data_list: List[str] = [
                data_dict.get('name', None),
                data_dict.get('genre', None),
                data_dict.get('duration', None),
                data_dict.get('synopsis', None),
                movie_id
            ]

            self.conn.connect()
            self.conn.cursor.execute(UPDATE_MOVIE, data_list)
            self.conn.connection.commit()
            self.conn.close()

            self.logger.info('ATUALIZANDO FILME POR ID')
            return movie_id

        except Exception as e:
            raise e
