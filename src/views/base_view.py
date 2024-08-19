from pydantic import ValidationError

from src.utils.token import Token
from src.utils.logger import Logger
from src.utils.inputs import Inputs
from src.utils.hashing import Hashing
from src.utils.printer import Printer
from src.utils.terminal import Terminal
from src.utils.handlers import Handlers


from src.crud.seats_crud import SeatsCrud
from src.crud.rooms_crud import RoomsCrud
from src.crud.movies_crud import MoviesCrud
from src.crud.admins_crud import AdminsCrud
from src.crud.clients_crud import ClientsCrud
from src.crud.persons_crud import PersonsCrud
from src.crud.tickets_crud import TicketsCrud
from src.crud.sessions_crud import SessionsCrud


class BaseView:
    def __init__(self):
        self.inputs: Inputs = Inputs()
        self.printer: Printer = Printer()
        self.terminal: Terminal = Terminal()

        self.seat_crud: SeatsCrud = SeatsCrud()
        self.room_crud: RoomsCrud = RoomsCrud()
        self.admin_crud: AdminsCrud = AdminsCrud()
        self.movie_crud: MoviesCrud = MoviesCrud()
        self.client_crud: ClientsCrud = ClientsCrud()
        self.person_crud: PersonsCrud = PersonsCrud()
        self.ticket_crud: TicketsCrud = TicketsCrud()
        self.session_crud: SessionsCrud = SessionsCrud()

        self.token: Token = Token()
        self.logger: Logger = Logger()
        self.hash: Hashing = Hashing()
        self.handlers: Handlers = Handlers()

    def logout(self) -> None:
        self.token.delete_token()
        self.logger.info('FAZENDO LOGOUT')

    def start(self) -> None:
        raise NotImplementedError(
            "Subclasses should implement start() method.")

    def invalid_option(self) -> None:
        self.printer.error('Opção inválida, tente novamente', clear=True)

    def invalid_value(self) -> None:
        self.printer.error('Valor inválido, tente novamente', clear=True)

    def crt_admin(self) -> None:
        while True:
            try:
                person_data = self.inputs.input_person()
                if person_data == None:
                    self.printer.warning(text='Cancelando...', clear=True)
                    return False

                self.person_crud.insert_person(person_data)
                person: tuple = self.person_crud.select_by_email(
                    person_data['email']
                )

                self.admin_crud.insert_admin(person[0])
                self.printer.success('Admin criado com sucesso!', clear=True)
                return True

            except ValidationError as e:
                self.handlers.handle_validation_error(e)

            except Exception as e:
                self.printer.error(f'Erro ao criar admin: {str(e)}')

    def close(self, text: str = 'Realmente deseja fechar?') -> bool:
        self.terminal.clear()

        confirm_options = ['Sim', 'Não']

        option = self.inputs.input_an_option(
            confirm_options,
            text=text)

        return option == 1
