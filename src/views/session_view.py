from src.views.base_view import BaseView
from src.crud.sessions_crud import SessionsCrud
from pydantic import ValidationError


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
                option: int = self.choose_an_option(
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
                    'PRICE',
                    'START TIME'
                ]
                movies_list: list = self.session_crud.select_all_sessions()
                movies_formated: list = [[
                    movie[0],
                    movie[1],
                    movie[2],
                    movie[3],
                    movie[4],
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
                    self.terminal.clear()
                    self.printer.success('Operação cancelada!')
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
                    break

                session: tuple = [self.session_crud.select_session_by_id(
                    session_id)]

                header = [
                    'SESSION ID',
                    'ROOM ID',
                    'MOVIE ID',
                    'PRICE',
                    'START TIME'
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

                session_id: str = input('Session ID: ')

                if session_id.lower() == 'q':
                    break

                confirm_session_id: str = self.session_crud.delete_session(
                    session_id)

                if session_id == confirm_session_id:
                    self.terminal.clear()
                    self.printer.success(
                        'Sessão deletada com sucesso!', timer=True)
                    self.terminal.clear()

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
                    break

                session: tuple = self.session_crud.select_session_by_id(
                    session_id)

                if not session:
                    self.printer.error(
                        text='Nenhuma sala identificada, tente novamente')
                    self.terminal.clear()
                    break

                old_data['room_id'] = session[1]
                old_data['movie_id'] = session[2]
                old_data['price'] = session[3]
                old_data['start_time'] = session[4]

                room_id: str = input(
                    'Room ID (deixe em branco para manter o atual): ').strip()
                movie_id: int = input(
                    'Movie ID (deixe em branco para manter o atual): ').strip()
                price: int = input(
                    'Price (deixe em branco para manter a atual): ').strip()
                start_time: str = input(
                    'Start Time (deixe em branco para manter a atual): ').strip()

                if not room_id:
                    new_data['room_id'] = old_data['room_id']
                else:
                    new_data['room_id'] = room_id

                if not movie_id:
                    new_data['movie_id'] = old_data['movie_id']
                else:
                    new_data['movie_id'] = movie_id

                if not price:
                    new_data['price'] = old_data['price']
                else:
                    new_data['price'] = price

                if not start_time:
                    new_data['start_time'] = old_data['start_time']
                else:
                    new_data['start_time'] = start_time

                if new_data:
                    self.session_crud.update_session(session_id, new_data)
                    self.printer.success('Sala atualizado com sucesso!')
                else:
                    self.printer.info(
                        'Nenhum dado fornecido para atualização.')

            except ValueError as e:
                self.terminal.clear()
                self.printer.error(f'{e}')
                self.terminal.clear()

            except Exception as e:
                self.printer.error(f'Erro ao atualizar sala: {e}')

            self.manager.session_view.start()
