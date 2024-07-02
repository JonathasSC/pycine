from src.utils.printer import Printer
from src.utils.terminal import Terminal


class Inputs:
    def __init__(self) -> None:
        self.printer: Printer = Printer()
        self.terminal: Terminal = Terminal()

    def input_login(self):
        person_data: dict = {}

        person_data['email'] = input('Email: ')
        person_data['password'] = input('Senha: ')

        return person_data

    def input_person(self):
        person_data: dict = {}

        person_data['name'] = input('Nome: ')
        person_data['email'] = input('Email: ')
        person_data['password'] = input('Senha: ')

        return person_data

    def input_movie(self):
        movie_data: dict = {}

        movie_data['name'] = input('Nome: ')
        movie_data['genre'] = input('Genre: ')
        movie_data['duration'] = input('Duration: ')
        movie_data['synopsis'] = input('Synopsis: ')

        return movie_data

    def input_room(self):
        room_data = {}

        room_data['name'] = input('Nome: ').strip()
        room_data['rows'] = int(input('Rows: '))
        room_data['columns'] = int(input('Columns: '))

        valid_types = ['normal', 'dubbed', 'subtitled', 'vip']

        self.terminal.clear()
        room_option: int = self.choose_an_option(
            valid_types, 'Escolha o tipo da sala:', cancel=True)
        if room_option is None:
            return None

        room_data['type'] = valid_types[room_option - 1]
        return room_data

    def input_session(self):
        session_data: dict = {}

        session_data['room_id'] = input('Room ID: ')
        session_data['movie_id'] = input('Movie ID: ')
        session_data['price'] = input('Price: ')
        session_data['start_time'] = input('Start time: ')

        return session_data

    def choose_an_option(self, options: list, text: str = 'Escolha uma opção', cancel: bool = False):
        while True:
            try:
                self.printer.generic(text, line=True)
                self.printer.option_list(options)

                if cancel:
                    self.printer.generic(f'[0] - Cancelar')
                option: int = int(input('Digite uma opção: '))

                if cancel and option == 0:
                    return None
                if 0 < option <= len(options) + 1:
                    return option
                else:
                    self.printer.error("Opção inválida. Tente novamente.")

            except ValueError:
                self.printer.error(
                    "Entrada inválida. Por favor, digite um número.")

    def execute_option(self, options: dict, option: int):
        action = options.get(option, self.invalid_option)
        action()

    def invalid_option(self):
        self.terminal.clear()
        self.printer.error('Opção inválida, tente novamente')
        self.terminal.clear()

    def invalid_value(self):
        self.terminal.clear()
        self.printer.error('Valor inválido, tente novamente')
        self.terminal.clear()
