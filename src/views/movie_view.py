from src.views.base_view import BaseView
from pydantic import ValidationError
from typing import Optional


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

                movie_name: str = input('Nome do filme: ').strip().lower()

                if movie_name.lower() == 'q':
                    self.printer.success('Exclusão cancelada', clear=True)
                    break

                confirm_del: str = self.movie_crud.delete_movie_by_name(
                    movie_name)

                if confirm_del:
                    self.printer.success(
                        text='Filme deletado com sucesso!',
                        clear=True)

            except ValueError as e:
                self.printer.error(f'{e}')

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
                    text='Preencha os campos, ou digite "q" para cancelar',
                    line=True
                )

                movie_name: str = input('Nome do filme: ').strip().lower()
                if movie_name == 'q':
                    self.printer.warning(
                        text='Cancelando...',
                        clear=True)
                    self.manager.movie_view.start()

                movie: tuple = self.movie_crud.select_movie_by_name(movie_name)

                if not movie:
                    self.printer.error(
                        text='Nenhum filme identificado, tente novamente')
                    self.terminal.clear()
                    self.manager.movie_view.put_movie()

                movie_id: str = movie[0]
                old_data['name'] = movie[1]
                old_data['genre'] = movie[2]
                old_data['duration'] = movie[3]
                old_data['synopsis'] = movie[4]

                new_data: Optional[dict] = self.inputs.input_movie()
                if new_data == None:
                    self.printer.warning(
                        text='Cancelando...',
                        clear=True)
                    self.manager.movie_view.put_movie()

                data: dict = {
                    'name': new_data.get('name') if new_data.get('name') != '' else old_data['name'],
                    'genre': new_data.get('genre') if new_data.get('genre') != '' else old_data['genre'],
                    'duration': new_data.get('duration') if new_data.get('duration') != '' else old_data['duration'],
                    'synopsis': new_data.get('synopsis') if new_data.get('synopsis') != '' else old_data['synopsis'],
                }

                self.movie_crud.update_movie(movie_id, data)
                self.printer.success(
                    'Filme atualizado com sucesso!',
                    clear=True)

            except ValueError as e:
                self.printer.error(f'{e}', clear=True)

            except Exception as e:
                self.printer.error(f'Erro ao atualizar filme: {e}', clear=True)

            finally:
                self.manager.movie_view.start()
