from src.views.base_view import BaseView
from src.utils.counters import maximum_room_capacity


class SeatView(BaseView):
    def __init__(self, manager):
        super().__init__()
        self.manager = manager
        self.maximum_room_capacity = maximum_room_capacity

        self.list_options: list = [
            'Adicionar nova cadeira',
            'Deletar cadeiras de uma sala',
            'Ver lista de assentos de sala',
            'Voltar'
        ]

    def start(self) -> None:
        while True:
            try:
                self.terminal.clear()
                option: int = self.choose_an_option(self.list_options)

                match option:
                    case 1:
                        self.crt_seat()
                    case 2:
                        self.del_seats_by_room_name()
                    case 3:
                        self.get_seats_by_room_name()
                    case 4:
                        self.manager.admin_view.admin_flow()
                    case _:
                        self.invalid_option()
                        self.start()

            except Exception as e:
                self.printer.error(f'Erro ao iniciar tela de tickets: {e}')

    def crt_seat(self) -> None:
        while True:

            try:
                seat_data = {}

                self.terminal.clear()
                self.printer.generic(
                    text='Preencha os campos ou digite "q" para cancelar',
                    line=True)

                room_id: str = input('Room ID: ')

                if room_id in 'Qq':
                    self.printer.warning(text='Cancelando...', clear=True)
                    break

                if not self.room_crud.select_room_by_id(room_id):
                    self.printer.warning(
                        text='Nenhuma sala identificada tente novamente',
                        clear=True)
                    continue

                if self.maximum_room_capacity(room_id):
                    raise ValueError('A sala já atingiu a capacidade máxima')

                options: list = ['Sim', 'Não']

                auto_create_seats: str = self.choose_an_option(
                    options=options,
                    text='Deseja criar cadeiras para essa sala automaticamente?'
                )

                if auto_create_seats == 1:
                    room: tuple = self.room_crud.select_room_by_id(room_id)
                    self.seat_crud.insert_seats_by_room(room)
                    self.printer.success('Cadeiras criadas com sucesso!')
                    break

                elif auto_create_seats == 2:
                    valid_states: list = [
                        'available',
                        'sold',
                        'reserved'
                    ]

                    seat_data['seat_code'] = input('Seat Code: ')
                    if seat_data['seat_code'] in 'Qq':
                        break

                    seat_data['row'] = int(input('Row: '))
                    if seat_data['row'] in 'Qq':
                        break

                    seat_data['col'] = int(input('Col: '))
                    if seat_data['col'] in 'Qq':
                        break

                    state_option: int = self.choose_an_option(
                        valid_states,
                        text='Escolha o estado da cadeira',
                        cancel=True
                    )

                    if not state_option:
                        self.manager.seat_view.start()

                    seat_data['state'] = seat_data[state_option - 1]
                    self.seat_crud.insert_seat(seat_data)
                    self.manager.seat_view.start()

                if not seat_data:
                    self.printer.warning(text='Cancelando...', clear=True)

            except ValueError as e:
                self.printer.error(
                    text=f'{e}',
                    clear=True)

            except Exception as e:
                self.printer.error(
                    text=f'Erro ao iniciar tela de cadeiras: {e}',
                    clear=True)
            finally:
                self.manager.seat_view.start()

    # def del_seats_by_room_name(self) -> None:
    #     while True:
    #         try:
    #             self.terminal.clear()

    #             self.printer.generic(
    #                 text='Preencha os campos ou digite "q" para cancelar',
    #                 line=True)
    #             room_name: str = input('Nome da sala: ')

    #             if room_name.lower() == 'q':
    #                 self.printer.warning(text='Cancelando...', clear=True)
    #                 self.manager.seat_view.start()

    #             if not self.room_crud.select_room_by_name(room_name):
    #                 self.printer.warning(
    #                     text='Nenhuma sala encontrada, tente novamente',
    #                     clear=True
    #                 )
    #                 self.manager.seat_view.del_seats_by_room_name()

    #             self.printer.success(
    #                 text=f'Cadeiras da {room_name} deletadas com sucesso!',
    #                 clear=True
    #             )

    #         except Exception as e:
    #             self.printer.error(f'Erro ao deletar cadeiras: {e}')

    #         finally:
    #             self.manager.seat_view.start()
    def del_seats_by_room_name(self) -> None:
        while True:
            try:
                self.terminal.clear()
                self.printer.generic(
                    text='Preencha os campos ou digite "q" para cancelar', line=True)

                room_name: str = input('Nome da sala: ').strip()

                if room_name.lower() == 'q':
                    self.printer.warning(text='Cancelando...', clear=True)
                    break

                if not self.room_crud.select_room_by_name(room_name):
                    self.printer.warning(text='Nenhuma sala encontrada, tente novamente',
                                         clear=True)
                    continue

                self.seat_crud.delete_seats_by_room_name(room_name)
                self.printer.success(text=f'Assentos deletadas com sucesso!',
                                     clear=True)
                break

            except Exception as e:
                self.printer.error(f'Erro ao deletar cadeiras: {e}')

        self.manager.seat_view.start()

    def get_seats_by_room_name(self) -> None:
        while True:
            try:
                self.terminal.clear()
                self.printer.generic(text='Preencha os campos ou digite "q" para cancelar',
                                     line=True)

                room_name: str = input('Nome da sala: ')

                if room_name.lower() == 'q':
                    self.printer.warning(text='Cancelando...', clear=True)
                    break

                if not self.room_crud.select_room_by_name(room_name):
                    self.printer.warning(
                        text='Nenhuma sala encontrada, tente novamente',
                        clear=True
                    )
                    continue

                header = [
                    'ID DO ASSENTO',
                    'ID DA SALA',
                    'CODIGO DO ASSENTO',
                    'LINHA',
                    'COLUNA',
                    'ESTADO'
                ]
                seats_list: list = self.seat_crud.select_seats_by_room_name(
                    room_name)
                self.printer.display_table(header, seats_list)

                break

            except Exception as e:
                self.printer.error(f'Erro ao deletar cadeiras: {e}')

            self.manager.seat_view.start()
