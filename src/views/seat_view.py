from src.views.base_view import BaseView


class SeatView(BaseView):
    def __init__(self, manager):
        super().__init__()
        self.manager = manager

        self.list_options: list = [
            'Adicionar nova cadeira',
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
                    self.terminal.clear()
                    self.printer.warning('Cancelando...')
                    break

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
                        break

                    seat_data['state'] = seat_data[state_option - 1]
                    self.seat_crud.insert_seat(seat_data)
                    break

                if not seat_data:
                    self.terminal.clear()
                    self.printer.warning('Cancelando...')
                    break

            except ValueError as e:
                self.printer.error(
                    text=f'{e}',
                    clear=True)

            except Exception as e:
                self.printer.error(
                    text=f'Erro ao iniciar tela de cadeiras: {e}',
                    clear=True)
