from src.views.base_view import BaseView
from pydantic import ValidationError
from typing import Optional


class RoomView(BaseView):
    def __init__(self, manager):
        super().__init__()
        self.manager = manager

        self.list_options: list = [
            'Adicionar nova sala',
            'Ver lista de salas',
            'Atualizar salas',
            'Deletar sala',
            'Voltar'
        ]

    def start(self) -> None:
        while True:
            try:
                self.terminal.clear()
                option: int = self.choose_an_option(self.list_options)

                match option:
                    case 1:
                        self.crt_room()
                    case 2:
                        self.get_rooms()
                    case 3:
                        self.put_room()
                    case 4:
                        self.del_room()
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
                    text='Preencha os campos ou digite "q" para cancelar',
                    line=True)

                room_data: dict = self.inputs.input_room()

                if not room_data:
                    self.printer.warning(text='Cancelando...', clear=True)
                    break

                auto_seat = ['Sim', 'Não']
                option: int = self.choose_an_option(
                    options=auto_seat,
                    text='Deseja criar cadeiras automaticamente? ',
                )

                if option == 1:
                    room_id: str = self.room_crud.insert_room(room_data)
                    room: tuple = self.room_crud.select_room_by_id(room_id)
                    self.seat_crud.insert_seats_by_room(room)
                else:
                    room_id: str = self.room_crud.insert_room(room_data)

                self.printer.success(
                    text='Sala criada com sucesso!',
                    clear=True)

                break

            except ValidationError as e:
                erro = e.errors()[0]
                message: str = erro['msg']
                self.printer.error(message[13:])

            except Exception as e:
                self.printer.error(f'Erro ao criar sala: {e}')

        self.manager.room_view.start()

    def get_rooms(self) -> None:
        while True:
            try:
                self.terminal.clear()
                header = ['ID', 'NAME', 'ROWS', 'COLUMNS', 'TYPE']
                rooms_list: list = self.room_crud.select_all_rooms()
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
                    text='Digite o nome da sala, ou "q" para cancelar',
                    line=True
                )

                name: str = input('Nome da sala: ').strip()

                if name.lower() == 'q':
                    self.printer.warning(
                        text='Cancelando...',
                        clear=True)
                    self.manager.room_view.start()

                room: Optional[tuple] = self.room_crud.select_room_by_name(
                    name)

                if not room:
                    self.printer.error(
                        text='Nenhuma sala identificada tente novamente', clear=True)
                    self.manager.room_view.put_room()

                old_data['name'] = room[1]
                old_data['rows'] = room[2]
                old_data['type'] = room[4]
                old_data['columns'] = room[3]

                new_data: Optional[dict] = self.inputs.input_put_room()

                if not new_data:
                    self.printer.warning(
                        text='Cancelando...',
                        clear=True)
                    self.manager.room_view.start()

                data: dict = {
                    'name': new_data.get('name') if new_data.get('name') != '' else old_data['name'],
                    'rows': new_data.get('rows') if new_data.get('rows') != '' else old_data['rows'],
                    'type': new_data.get('type') if new_data.get('type') != '' else old_data['type'],
                    'columns': new_data.get('columns') if new_data.get('columns') != '' else old_data['columns'],
                }

                self.room_crud.update_room_by_name(name, data)

            except ValueError as e:
                self.terminal.clear()
                self.printer.error(f'{e}')
                self.terminal.clear()

            except Exception as e:
                self.printer.error(f'Erro ao atualizar sala: {e}')

            self.manager.room_view.start()

    def del_room(self) -> None:
        while True:
            try:
                self.terminal.clear()
                self.printer.generic(
                    text='Preencha os campos ou digite "q" para cancelar',
                    line=True)

                room_name: str = input('Nome da sala: ').strip()

                if room_name.lower() == 'q':
                    break

                if self.room_crud.delete_room_by_name(room_name) and self.seat_crud.delete_seats_by_room_name(room_name):
                    self.printer.success(text='Filme deletado com sucesso!',clear=True)

            except ValueError as e:
                self.printer.error(text=f'{e}',
                                   clear=True)
                self.manager.room_view.del_room()

            except Exception as e:
                self.printer.error(text=f'Erro ao deletar filme: {e}',
                                   clear=True)

                self.manager.room_view.del_room()

            finally:
                self.manager.room_view.start()
