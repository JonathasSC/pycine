from src.views.base_view import BaseView
from src.crud.rooms_crud import RoomsCrud


class RoomView(BaseView):
    def __init__(self):
        super().__init__()
        self.rooms_crud: RoomsCrud = RoomsCrud()
        self.before_view = None

        self.list_options: list = [
            'Adicionar nova sala',
            'Adicionar nova sala com assentos',
            'Ver lista de salas',
            'Voltar'
        ]

        self.option_actions = {
            1: self.create_room,
            2: self.create_room_with_seats,
            3: self.list_rooms,
            3: self.back_to_admin
        }

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

    def back_to_admin(self):
        if self.before_view:
            self.before_view.start()
        self.printer.error('AdminView não definida')

    def create_room(self):
        while True:
            try:
                self.terminal.clear()
                self.printer.generic(
                    'Coloque os campos de uma nova sala',
                    line=True
                )

                room_data: dict = self.inputs.input_room()
                self.rooms_crud.insert_room(room_data)
                self.printer.success('Sala adicionada com sucesso!')
                break

            except Exception as e:
                self.printer.error(f'Erro ao criar sala: {e}')
                break

        self.start()

    def create_room_with_seats(self):
        while True:
            try:
                self.terminal.clear()
                self.printer.generic(
                    'Coloque os campos de uma nova sala',
                    line=True
                )
                room_data: dict = self.inputs.input_room()
                if room_data:
                    self.rooms_crud.insert_room_with_seats(room_data)
                    self.printer.success('Sala adicionada com sucesso!')
                    break

                self.start()
            except Exception as e:
                self.printer.error(f'Erro ao criar sala: {e}')
                break

        self.start()

    def list_rooms(self):
        while True:
            try:
                self.terminal.clear()
                header = ['ID', 'NAME', 'ROWS', 'COLUMNS', 'TYPE']
                rooms_list: list = self.rooms_crud.select_all_rooms()
                self.printer.display_table(header, rooms_list)
                break

            except Exception as e:
                self.terminal.clear()
                self.printer.error(f'Erro ao mostrar salas {e}')
                break

        self.start()

    def put_room(self):
        while True:
            try:
                self.terminal.clear()
                self.printer.generic(
                    'Coloque os novos campos da sala', line=True)
                room_data: dict = self.inputs.input_room()
                room_data['room_id'] = input('Room id: ')

            except Exception as e:
                self.terminal.clear()
                self.printer.error(f'Erro ao atualizar sala {e}')
                break
