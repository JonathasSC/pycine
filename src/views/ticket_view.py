from src.views.base_view import BaseView


class TicketView(BaseView):
    def __init__(self, manager):
        super().__init__()
        self.manager = manager

        self.list_options: list = [
            'Adicionar novo ticket',
            'Deletar ticket',
            'Ver ticket',
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
                        self.del_ticket()
                    case 3:
                        self.get_ticket()
                    case 4:
                        self.manager.admin_view.admin_flow()
                    case _:
                        self.invalid_option()
                        self.start()

            except Exception as e:
                self.printer.error(f'Erro ao iniciar tela de tickets: {e}')

    def crt_ticket(self) -> None:
        while True:
            try:
                ticket_data = {}

                self.terminal.clear()
                self.printer.generic(
                    text='Preencha os campos ou digite "q" para cancelar',
                    line=True)

                ticket_data['session_id'] = input('Session ID: ').strip()
                if ticket_data['session_id'] in 'Qq':
                    self.printer.warning(text='Cancelando...', clear=True)
                    break

                if not self.session_crud.select_session_by_id(ticket_data['session_id']):
                    raise ValueError(
                        'Nenhuma sessão com esse ID foi encontrad.')

                ticket_data['person_id'] = input('Person ID: ').strip()
                if ticket_data['person_id'] in 'Qq':
                    self.printer.warning(text='Cancelando...', clear=True)
                    break

                if not self.person_crud.select_by_id(ticket_data['person_id']):
                    raise ValueError(
                        'Nenhuma pessoa com esse ID foi encontrada.')

                ticket_data['seat_id'] = input('Seat ID: ').strip()
                if ticket_data['seat_id'] in 'Qq':
                    self.printer.warning(text='Cancelando...', clear=True)
                    break

                seat: tuple = self.seat_crud.select_seat_by_id(
                    ticket_data['seat_id'])

                if not seat:
                    raise ValueError(
                        'Nenhum assento com esse ID foi encontrada.')

                if seat[5] == 'sold':
                    raise ValueError('Essa cadeira já foi vendida')

                if self.ticket_crud.insert_ticket(ticket_data):
                    self.seat_crud.update_seat_state(ticket_data['seat_id'],
                                                     'sold')
                    self.printer.success(text='Ticket criado com sucesso!',
                                         clear=True)

            except ValueError as e:
                self.printer.error(text=f'{e}', clear=True)

            except Exception as e:
                self.printer.error(
                    text=f'Erro ao tentar criar ticket: {e}',
                    clear=True)

            continue

    def del_ticket(self) -> None:
        while True:
            try:
                self.terminal.clear()
                self.printer.generic(
                    text='Preencha os campos ou digite "q" para cancelar',
                    line=True)

                ticket_id: str = input('Ticket ID: ').strip()

                if ticket_id.lower() == 'q':
                    self.printer.warning(text='Cancelando...', clear=True)
                    break

                self.ticket_crud.delete_ticket_by_id(ticket_id)
                self.printer.success('Ticket deletado com sucesso!')

            except ValueError as e:
                self.printer.error(
                    text=f'{e}',
                    clear=True)

            except Exception as e:
                self.printer.error(
                    text=f'Erro ao deletar criar ticket: {e}',
                    clear=True)

    def get_ticket(self) -> None:
        while True:
            try:
                self.terminal.clear()
                self.printer.generic(
                    text='Preencha os campos ou digite "q" para cancelar',
                    line=True)

                ticket_id: str = input('Ticket ID: ').strip()

                if ticket_id.lower() == 'q':
                    break

                ticket: tuple = [
                    self.ticket_crud.select_ticket_by_id(ticket_id)
                ]

                if not ticket:
                    from time import sleep
                    print('Ue')
                    sleep(4)
                    raise ValueError(
                        'Nenhum ticket com esse ID foi encontrado')

                header = [
                    'TICKET ID',
                    'SEAT ID',
                    'PERSON ID',
                    'SESSION ID'
                ]

                self.printer.display_table(header, ticket)
                self.start()

            except ValueError as e:
                self.printer.error(
                    text=f'{e}',
                    clear=True)

            except Exception as e:
                self.printer.error(
                    text=f'Erro ao pegar ticket: {e}',
                    clear=True)
