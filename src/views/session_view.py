from src.views.base_view import BaseView
from src.crud.sessions_crud import SessionsCrud
from pydantic import ValidationError
from typing import Optional


class SessionView(BaseView):
    def __init__(self, manager):
        super().__init__()
        self.before_view = None
        self.manager = manager
        self.session_crud: SessionsCrud = SessionsCrud()

        self.list_options: list = [
            'Adicionar nova sessão',
            'Ver lista de sessões',
            'Ver sessão',
            'Deletar sessão',
            'Atualizar sessão',
            'Voltar'
        ]

    def start(self) -> None:
        while True:
            try:
                self.terminal.clear()
                option: int = self.inputs.input_an_option(
                    self.list_options, text='Escolha o que gerenciar')

                match option:
                    case 1:
                        self.crt_session()
                    case 2:
                        self.get_sessions()
                    case 3:
                        self.get_session()
                    case 4:
                        self.del_session()
                    case 5:
                        self.put_session()
                    case 6:
                        self.manager.admin_view.admin_flow()
                    case _:
                        self.invalid_option()
                        self.start()

            except Exception as e:
                self.printer.error(f'Erro ao iniciar tela de salas: {e}')

    def get_sessions(self) -> None:
        while True:
            try:
                self.terminal.clear()
                header = [
                    'SESSION ID',
                    'ROOM ID',
                    'MOVIE ID',
                    'PRICE (R$)',
                    'START DATE',
                    'START TIME',
                ]
                movies_list: list = self.session_crud.select_all_sessions()
                movies_formated: list = [[
                    movie[0],
                    movie[1],
                    movie[2],
                    movie[3],
                    movie[4],
                    movie[5],
                ] for movie in movies_list]

                self.printer.display_table(header, movies_formated)
                self.start()

            except Exception as e:
                self.printer.error(f'Erro ao iniciar sessões: {e}')
                self.start()

    def crt_session(self) -> None:
        while True:
            try:
                self.terminal.clear()

                self.printer.generic(
                    text='Preencha os campos (ou digite "q" para cancelar)',
                    line=True
                )

                session_data: dict = self.inputs.input_session()

                if not session_data:
                    self.printer.warning(text='Cancelando...',
                                         clear=True)
                    self.manager.session_view.start()

                self.session_crud.insert_session(session_data)
                self.printer.success('Sessão adicionada com sucesso!')

            except ValidationError as e:
                erro = e.errors()[0]
                message: str = erro['msg']
                self.printer.error(message[13:])

            except Exception as e:
                self.printer.error(f'Erro ao criar sessão: {e}')

            finally:
                self.manager.session_view.start()

    def get_session(self) -> None:
        while True:
            try:
                self.terminal.clear()
                self.printer.generic(
                    text='Preencha os campos ou digite "q" para cancelar',
                    line=True)

                session_id: str = input('Session ID: ')

                if session_id.lower() == 'q':
                    self.printer.warning(text='Cancelando...', clear=True)
                    break

                session: tuple = [self.session_crud.select_session_by_id(
                    session_id)]

                header = [
                    'SESSION ID',
                    'ROOM ID',
                    'MOVIE ID',
                    'PRICE',
                    'START DATE',
                    'START TIME',
                ]

                self.printer.display_table(header, session)
                self.start()

            except ValidationError as e:
                erro = e.errors()[0]
                message: str = erro['msg']
                self.printer.error(message[13:])

            except Exception as e:
                self.printer.error(f'Erro ao criar sessão: {e}')

            finally:
                self.manager.session_view.start()

    def del_session(self) -> None:
        while True:
            try:
                self.terminal.clear()
                self.printer.generic(
                    text='Preencha os campos ou digite "q" para cancelar',
                    line=True)

                session_id: str = input('Session ID: ').strip()

                if session_id.lower() == 'q':
                    self.printer.warning(text='Cancelando...', clear=True)
                    break

                if not self.session_crud.delete_session(session_id):
                    self.printer.error(
                        text='Nenhuma sessão encontrada, tente novamente',
                        clear=True
                    )
                    self.manager.session_view.del_session()

                self.printer.success(
                    text='Sessão deletada com sucesso!',
                    clear=True
                )

            except Exception as e:
                self.printer.error(f'Erro ao deletar filme: {e}')

            finally:
                self.manager.session_view.start()

    def put_session(self) -> None:
        while True:
            try:
                old_data: dict = {}
                new_data: dict = {}

                self.terminal.clear()
                self.printer.generic(
                    text='Digite o Session ID, ou "q" para cancelar',
                    line=True
                )

                session_id: str = input('Session ID: ').strip()
                if session_id.lower() == 'q':
                    self.printer.warning(text='Cancelando...', clear=True)
                    self.manager.session_view.start()

                session: tuple = self.session_crud.select_session_by_id(
                    session_id)

                if not session:
                    self.printer.error(
                        text='Nenhuma sessão encontrada, tente novamente',
                        clear=True
                    )
                    self.put_session()

                old_data['price'] = session[3]
                old_data['room_id'] = session[1]
                old_data['movie_id'] = session[2]
                old_data['start_date'] = session[4]
                old_data['start_time'] = session[5]

                new_data: Optional[dict] = self.inputs.input_put_session()

                if not new_data:
                    self.printer.warning(text='Cancelando...', clear=True)
                    self.manager.movie_view.start()

                data: dict = {
                    'price': new_data.get('price') if new_data.get('price') != '' else old_data['price'],
                    'room_id': new_data.get('room_id') if new_data.get('room_id') != '' else old_data['room_id'],
                    'movie_id': new_data.get('movie_id') if new_data.get('movie_id') != '' else old_data['movie_id'],
                    'start_date': new_data.get('start_date') if new_data.get('start_date') != '' else old_data['start_date'],
                    'start_time': new_data.get('start_time') if new_data.get('start_time') != '' else old_data['start_time'],
                }

                self.session_crud.update_session(session_id, data)
                self.printer.success(
                    text='Sessão atualizada com sucesso!',
                    clear=True
                )

            except ValueError as e:
                self.printer.error(f'{e}', clear=True)

            except Exception as e:
                self.printer.error(f'Erro ao atualizar sessão: {e}')
