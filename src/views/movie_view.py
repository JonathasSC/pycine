from src.views.base_view import BaseView


class MovieView(BaseView):
    def __init__(self, manager):
        super().__init__()
        self.manager = manager

        self.list_options: list = [
            'Adicionar novo filme',
            'Ver lista de filmes',
            'Deletar filme',
            'Atualizar filme',
            'Voltar',
        ]

    def start(self) -> None:
        while True:
            try:
                self.terminal.clear()
                option: int = self.choose_an_option(self.list_options)

                match option:
                    case 1:
                        self.crt_movie()
                    case 2:
                        self.get_movies()
                    case 3:
                        self.del_movie()
                    case 4:
                        self.put_movie()
                    case 5:
                        self.manager.admin_view.admin_flow()
                    case _:
                        self.invalid_option()
                        self.start()

                break

            except Exception as e:
                self.printer.error(f'Erro ao iniciar movie view {e}')
                self.exit()

    def crt_movie(self) -> None:
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

    def get_movies(self) -> None:
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

    def del_movie(self) -> None:
        while True:
            try:
                self.terminal.clear()
                self.printer.generic(
                    text='Preencha os campos ou digite "q" para cancelar',
                    line=True)

                movie_id: str = input('Movie ID: ')

                if movie_id.lower() == 'q':
                    break

                confirm_movie_id: str = self.movie_crud.delete_movie(movie_id)

                if movie_id == confirm_movie_id:
                    self.terminal.clear()
                    self.printer.success('Filme deletado com sucesso!')
                    self.terminal.clear()

            except Exception as e:
                self.printer.error(f'Erro ao deletar filme: {e}')

            finally:
                self.manager.movie_view.start()

    def put_movie(self) -> None:
        while True:
            try:
                old_data: dict = {}
                new_data: dict = {}

                self.terminal.clear()
                self.printer.generic(
                    text='Digite o Movie ID, ou "q" para cancelar',
                    line=True
                )

                movie_id: str = input('Movie ID: ').strip().lower()

                if movie_id == 'q':
                    self.manager.movie_view.start()

                movie: tuple = self.movie_crud.select_movie_by_id(movie_id)

                if not movie:
                    self.printer.error(
                        text='Nenhum filme identificado, tente novamente')
                    self.terminal.clear()
                    self.manager.movie_view.put_movie()

                old_data['name'] = movie[1]
                old_data['genre'] = movie[2]
                old_data['duration'] = movie[3]
                old_data['synopsis'] = movie[4]

                from time import sleep

                print(movie)

                sleep(4)

                name: str = input(
                    'Nome (deixe em branco para manter o atual): ').strip()
                genre: str = input(
                    'Genero (deixe em branco para manter o atual): ').strip()
                duration: str = input(
                    'Duração (deixe em branco para manter a atual): ').strip()
                synopsis: str = input(
                    'Synopsis (deixe em branco para manter a atual): ').strip()

                if not name:
                    new_data['name'] = old_data['name']
                else:
                    new_data['name'] = name

                if not genre:
                    new_data['genre'] = old_data['genre']
                else:
                    new_data['genre'] = genre

                if not duration:
                    new_data['duration'] = old_data['duration']
                else:
                    new_data['duration'] = duration

                if not synopsis:
                    new_data['synopsis'] = old_data['synopsis']
                else:
                    new_data['synopsis'] = synopsis

                if new_data:
                    self.movie_crud.update_movie(movie_id, new_data)
                    self.printer.success('Admin atualizado com sucesso!')
                else:
                    self.printer.info(
                        'Nenhum dado fornecido para atualização.')

            except ValueError as e:
                self.terminal.clear()
                self.printer.error(f'{e}')
                self.terminal.clear()

            except Exception as e:
                self.printer.error(f'Erro ao atualizar filme: {e}')

            finally:
                self.manager.movie_view.start()
