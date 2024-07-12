from src.views.base_view import BaseView
from src.crud.sessions_crud import SessionsCrud


class SessionView(BaseView):
    def __init__(self, manager):
        super().__init__()
        self.before_view = None
        self.manager = manager
        self.session_crud: SessionsCrud = SessionsCrud()

        self.list_options: list = [
            'Adicionar nova sessão',
            'Ver lista de sessões',
            'Voltar'
        ]

    def list_sessions(self):
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

    def start(self):
        while True:
            try:
                self.terminal.clear()
                option: int = self.choose_an_option(
                    self.list_options, text='Escolha o que gerenciar')

                if option == 1:
                    self.create_session()
                    self.start()

                elif option == 2:
                    self.list_sessions()
                    self.start()

                elif option == 3:
                    self.manager.admin_view.admin_flow()

                else:
                    self.invalid_option()
                    continue

                break

            except Exception as e:
                self.printer.error(f'Erro ao iniciar tela de salas: {e}')

    def create_session(self):
        while True:
            try:
                self.terminal.clear()
                self.printer.generic('Enter new session fields', line=True)
                session_data: dict = self.inputs.input_session()
                self.session_crud.insert_session(session_data)
                self.printer.success('Sala adicionada com sucesso!')
                break

            except Exception as e:
                self.printer.error(f'Erro ao criar sessão: {e}')
                break
