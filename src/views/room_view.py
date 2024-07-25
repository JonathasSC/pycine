from src.views.base_view import BaseView
from src.crud.rooms_crud import RoomsCrud


class RoomView(BaseView):
    def __init__(self, manager):
        super().__init__()
        self.rooms_crud: RoomsCrud = RoomsCrud()
        self.before_view = None
        self.manager = manager

        self.list_options: list = [
            'Adicionar nova sala',
            'Adicionar nova sala com assentos',
            'Ver lista de salas',
            'Voltar'
        ]

    def set_before_view(self, view):
        self.before_view = view

    def start(self) -> None:
        while True:
            try:
                self.terminal.clear()
                option: int = self.choose_an_option(self.list_options)

                match option:
                    case 1:
                        self.crt_room()
                    case 2:
                        self.crt_room_with_seats()
                    case 3:
                        self.get_rooms()
                    case 4:
                        self.manager.admin_view.admin_flow()
                    case _:
                        self.invalid_option()
                        self.start()

            except Exception as e:
                self.printer.error(f'Erro ao iniciar tela de salas: {e}')

    def crt_room(self) -> None:
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

    def crt_room_with_seats(self) -> None:
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

    def get_rooms(self) -> None:
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

    def put_room(self) -> None:
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
