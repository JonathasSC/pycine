from src.views.base_view import BaseView


class TicketView(BaseView):
    def __init__(self, manager):
        super().__init__()
        self.manager = manager

        self.list_options: list = [
            'Adicionar novo ticket',
            'Voltar'
        ]

    def start(self) -> None:
        while True:
            try:
                self.terminal.clear()
                option: int = self.choose_an_option(self.list_options)

                match option:
                    case 1:
                        self.crt_ticket()
                    case 2:
                        self.manager.admin_view.admin_flow()
                    case _:
                        self.invalid_option()
                        self.start()

            except Exception as e:
                self.printer.error(f'Erro ao iniciar tela de tickets: {e}')

    def crt_ticket(self) -> None:
        while True:

            try:
                seat_data = {}

                self.terminal.clear()
                self.printer.generic(
                    text='Preencha os campos ou digite "q" para cancelar',
                    line=True)

                seat_data['session_id'] = input('Session ID: ')

                if seat_data['session_id'] in 'Qq':
                    self.printer.warning(text='Cancelando...', clear=True)
                    break

                if not self.session_crud.select_session_by_id(seat_data['session_id']):
                    self.printer.warning(
                        text='Nenhuma sessão com esse ID foi encontrada.',
                        clear=True)
                    continue

                seat_data['person_id'] = input('Person ID: ')

                if seat_data['person_id'] in 'Qq':
                    self.printer.warning(text='Cancelando...', clear=True)
                    break

                if not self.person_crud.select_by_id(seat_data['person_id']):
                    self.printer.warning(
                        text='Nenhuma sessão com esse ID foi encontrada.',
                        clear=True)
                    continue

                seat_data['seat_id'] = input('Seat ID: ')

                if seat_data['seat_id'] in 'Qq':
                    self.printer.warning(text='Cancelando...', clear=True)
                    break

                if not self.seat_crud.select_seat_by_id(seat_data['seat_id']):
                    self.printer.warning(
                        text='Nenhuma sessão com esse ID foi encontrada.',
                        clear=True)
                    continue

            except ValueError as e:
                self.printer.error(
                    text=f'{e}',
                    clear=True)

            except Exception as e:
                self.printer.error(
                    text=f'Erro ao iniciar tela de cadeiras: {e}',
                    clear=True)
