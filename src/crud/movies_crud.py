from src.crud.base_crud import BaseCrud
from src.queries.movies_queries import SELECT_ALL_MOVIES
from src.database.conn import Connection


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
