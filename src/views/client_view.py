from src.views.base_view import BaseView
from src.crud.movies_crud import MoviesCrud


class ClientView(BaseView):
    def __init__(self):
        super().__init__()

        self.movies_crud: MoviesCrud = MoviesCrud()

        self.list_options: list = [
            'Comprar ingresso',
            'Ver filmes em exibição',
            'Sair'
        ]

        self.option_actions = {
            1: self.buy_ticket,
            2: self.view_movie_poster,
            3: self.exit
        }

    def start(self):
        self.terminal.clear()
        self.printer.generic('Choice a option', line=True)
        option: int = self.choose_an_option(self.list_options)
        self.execute_option(self.option_actions, option)

    def buy_ticket(self):
        print('Comprando ticket...')

    def view_movie_poster(self):
        self.terminal.clear()
        self.printer.generic(text='Filmes em cartaz', line=True)
        try:
            movies_list: list = self.movies_crud.select_all_movies()
            for movie in movies_list:
                print(movie[1])
        except Exception as e:
            print(f'Erro ao mostrar filmes {e}')
