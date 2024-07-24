from src.views.base_view import BaseView


class MovieView(BaseView):
    def __init__(self, manager):
        super().__init__()
        self.manager = manager

        self.list_options: list = [
            'Adicionar novo filme',
            'Ver lista de filmes',
            'Voltar',
        ]

        self.option_actions = {
            1: self.create_movie,
            2: self.list_movies,
            3: self.manager.admin_view.admin_flow
        }

    def start(self):
        while True:
            try:
                self.terminal.clear()
                option: int = self.choose_an_option(self.list_options)
                self.execute_option(self.option_actions, option)
                break

            except Exception as e:
                self.printer.error(f'Erro ao iniciar movie view {e}')
                self.exit()

    def create_movie(self):
        while True:
            try:
                self.terminal.clear()
                self.printer.generic(
                    text='Preencha os campos (ou digite "q" para cancelar)',
                    line=True
                )

                movie_data: dict = self.inputs.input_movie()

                if not movie_data:
                    self.terminal.clear()
                    self.printer.success('Operação cancelada!')
                    self.manager.movie_view.start()

                self.movie_crud.insert_movie(movie_data)
                self.printer.success('Filme adicionado com sucesso!')
                self.manager.movie_view.start()

            except ValidationError as e:
                erro = e.errors()[0]
                message: str = erro['msg']
                self.printer.error(message[13:])

            except Exception as e:
                self.printer.error(f'Erro ao criar filme: {e}')
                self.manager.movie_view.start()

    def list_movies(self):
        while True:
            try:
                self.terminal.clear()
                header = ['ID', 'NAME', 'GENRE', 'DURATION', 'SYNOPSIS']
                movies_list: list = self.movie_crud.select_all_movies()
                movies_formated: list = [[
                    movie[0],
                    movie[1],
                    movie[2],
                    movie[3],
                    f'{str(movie[4])[:50]}...'
                ] for movie in movies_list]

                self.printer.display_table(header, movies_formated)
                self.start()

            except Exception as e:
                self.printer.error(f'Erro ao mostrar filmes: {e}')
                self.start()
