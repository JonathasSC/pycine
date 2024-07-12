from src.views.base_view import BaseView
from src.crud.sessions_crud import SessionsCrud


class SessionView(BaseView):
    def __init__(self):
        super().__init__()
        self.before_view = None
        self.session_crud: SessionsCrud = SessionsCrud()

        self.list_options: list = [
            'Adicionar nova sessão',
            'Ver lista de sessões',
            'Voltar'
        ]

        self.option_actions = {
            1: self.create_session,
            2: self.list_sessions,
            3: self.back_to_admin
        }

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

    def back_to_admin(self):
        if self.before_view:
            self.before_view.start()
        self.printer.error('AdminView não definida')

    def set_back_view(self, view):
        self.before_view = view

    def start(self):
        while True:
            try:
                self.terminal.clear()
                option: int = self.choose_an_option(self.list_options)
                self.execute_option(self.option_actions, option)
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

        self.start()
