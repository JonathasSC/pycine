from src.views.base_view import BaseView


class SessionView(BaseView):
    def __init__(self):
        super().__init__()
        self.before_view = None

        self.list_options: list = [
            'Adicionar nova sessão',
            'Sair'
        ]

        self.option_actions = {
            1: self.create_session,
            3: self.exit
        }

    def back_to_admin(self):
        if self.before_view:
            self.before_view.start()
        self.printer.error('AdminView não definida')

    def set_before_view(self, view):
        self.before_view = view

    def start(self):
        while True:
            try:
                self.terminal.clear()
                self.printer.generic('Choice a option', line=True)
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
