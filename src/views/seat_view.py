from src.views.base_view import BaseView


class SeatView(BaseView):
    def __init__(self, manager):
        super().__init__()
        self.manager = manager

        self.list_options: list = [
            'Adicionar novo ticket',
            'Ver lista de tickets',
            'Atualizar tickets',
            'Voltar'
        ]

    def start(self) -> None:
        while True:
            try:
                self.terminal.clear()
                option: int = self.choose_an_option(self.list_options)

                match option:
                    case 1:
                        self.crt_tickets()
                    case 2:
                        self.get_ticketss()
                    case 3:
                        self.put_tickets()
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

                seat_data['room_id']: str = input('Room ID')

                if seat_data['room_id'] in 'Qq':
                    self.terminal.clear()
                    self.printer.warning('Cancelando...')
                    break

                options: list = ['Sim', 'Não']
                auto_create_seats: str = self.choose_an_option(
                    options=options,
                    text='Deseja criar cadeiras para essa sala automaticamente?'
                )

                if auto_create_seats == 1:
                    pass

                elif auto_create_seats == 2:
                    valid_states: list = [
                        'available',
                        'sold',
                        'reserved'
                    ]

                    seat_data['seat_code']: str = input('Seat Code')
                    if seat_data['seat_code'] in 'Qq':
                        break

                    seat_data['row']: int = int(input('Row'))
                    if seat_data['row'] in 'Qq':
                        break

                    seat_data['col']: str = int(input('Col'))
                    if seat_data['col'] in 'Qq':
                        break

                    state_option: int = self.choose_an_option(
                        valid_states,
                        text='Escolha o estado da cadeira',
                        cancel=True
                    )

                    if not state_option:
                        break

                    seat_data['state']: str = seat_data[state_option - 1]
                    self.seat_crud.insert_seat(seat_data)
                    break

                if not seat_data:
                    self.terminal.clear()
                    self.printer.warning('Cancelando...')
                    break

            except Exception as e:
                self.printer.error(f'Erro ao iniciar tela de cadeiras: {e}')
