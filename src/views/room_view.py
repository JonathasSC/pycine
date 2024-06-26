from src.views.base_view import BaseView
from src.crud.rooms_crud import RoomsCrud


class RoomView(BaseView):
    def __init__(self):
        super().__init__()
        self.rooms_crud: RoomsCrud = RoomsCrud()

        self.list_options: list = [
            'Adicionar nova sala',
            'Ver lista de salas',
            'Sair'
        ]

        self.option_actions = {
            1: self.create_room,
            2: self.list_rooms,
            3: self.exit
        }

    def start(self):
        try:
            self.terminal.clear()
            self.printer.generic('Choice a option', line=True)
            option: int = self.choose_an_option(self.list_options)
            self.execute_option(self.option_actions, option)
        except Exception as e:
            self.printer.error(f'Erro ao iniciar tela de salas: {e}')

    def create_room(self):
        while True:
            try:
                self.terminal.clear()
                self.printer.generic('Enter new room fields', line=True)
                room_data: dict = self.inputs.input_room()
                self.rooms_crud.insert_room(room_data)
                self.printer.success('Sala adicionada com sucesso!')
                break

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

                input('Voltar? [press enter]')
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
                self.printer.generic('Enter new room fields', line=True)
                room_data: dict = self.inputs.input_room()
                room_data['room_id'] = input('Room id: ')

            except Exception as e:
                self.terminal.clear()
                self.printer.error(f'Erro ao atualizar sala {e}')
                break
