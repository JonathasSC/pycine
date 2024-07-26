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
            'Atualizar salas',
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
                        self.put_room()
                    case 5:
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
                old_data: dict = {}
                new_data: dict = {}

                self.terminal.clear()
                self.printer.generic(
                    text='Digite o Room ID, ou "q" para cancelar',
                    line=True
                )

                room_id: str = input('Room ID: ').strip().lower()

                if room_id == 'q':
                    self.manager.room_view.put_room()

                room: tuple = self.room_crud.select_by_room_id(room_id)

                if not room:
                    self.printer.error(
                        text='Nenhuma sala identificada, tente novamente')
                    self.terminal.clear()
                    self.manager.room_view.put_room()

                old_data['name'] = room[1]
                old_data['rows'] = room[2]
                old_data['columns'] = room[3]
                old_data['type'] = room[4]

                name: str = input(
                    'Nome (deixe em branco para manter o atual): ').strip()
                rows: int = input(
                    'Rows (deixe em branco para manter o atual): ').strip()
                columns: int = input(
                    'Colunas (deixe em branco para manter a atual): ').strip()
                _type: str = input(
                    'Type (deixe em branco para manter a atual): ').strip()

                if not name:
                    new_data['name'] = old_data['name']
                else:
                    new_data['name'] = name

                if not rows:
                    new_data['rows'] = old_data['rows']
                else:
                    new_data['rows'] = rows

                if not columns:
                    new_data['columns'] = old_data['columns']
                else:
                    new_data['columns'] = columns

                if not _type:
                    new_data['type'] = old_data['type']
                else:
                    new_data['type'] = _type

                if new_data:
                    self.room_crud.update_room(room_id, new_data)
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

            finally:
                self.manager.room_view.start()
