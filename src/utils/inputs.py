from src.utils.printer import Printer
from src.utils.terminal import Terminal
import getpass

from src.utils.validators import password_validator


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
        if person_data['name'] == 'q':
            return None

        person_data['email'] = input('Email: ')
        if person_data['email'] == 'q':
            return None

        person_data['password'] = self.input_password()
        if person_data['password'] == 'q':
            return None

        return person_data

    def input_register(self):
        person_data: dict = {}

        person_data['name'] = input('Nome: ')
        person_data['email'] = input('Email: ')
        person_data['password'] = self.input_password()

        return person_data

    def input_password(self):
        while True:
            password = getpass.getpass('Senha (ela está ocultada): ')
            confirm_password: str = getpass.getpass('Confirme a senha: ')

            if password != confirm_password:
                self.printer.error('Senhas não correspondem, tente novamente')
                pass

            elif not password_validator(password):
                self.terminal.clear()
                self.printer.password_params()

                self.terminal.clear()
                self.printer.warning('Tente novamente')
                self.terminal.clear()

            else:
                return password

    def input_movie(self):
        movie_data: dict = {}

        movie_data['name'] = input('Nome: ')
        if movie_data['name'] == 'q':
            return None

        movie_data['genre'] = input('Genre: ')
        if movie_data['genre'] == 'q':
            return None

        movie_data['duration'] = input('Duration: ')
        if movie_data['duration'] == 'q':
            return None

        movie_data['synopsis'] = input('Synopsis: ')
        if movie_data['synopsis'] == 'q':
            return None

        return movie_data

    def input_room(self):
        room_data = {}

        room_data['name'] = input('Nome: ').strip()
        room_data['rows'] = int(input('Rows: '))
        room_data['columns'] = int(input('Columns: '))

        valid_types = ['normal', 'dubbed', 'subtitled', 'vip']

        self.terminal.clear()
        room_option: int = self.choose_an_option(
            valid_types,
            'Escolha o tipo da sala:',
            cancel=True
        )

        if room_option:
            room_data['type'] = valid_types[room_option - 1]
            return room_data

        return None

    def input_session(self):
        session_data: dict = {}

        session_data['price'] = input('Price: ')
        session_data['room_id'] = input('Room ID: ')
        session_data['movie_id'] = input('Movie ID: ')
        session_data['start_time'] = input('Start time: ')

        return session_data

    def choose_an_option(self, options: list, text: str = 'Escolha uma opção', cancel: bool = False, clear: bool = True):
        while True:
            if clear:
                self.terminal.clear()

            self.printer.generic(text, line=True)
            self.printer.option_list(options)
            valid_range = range(0, len(options) + 1)

            if cancel:
                self.printer.generic('[0] - Cancelar')
            self.printer.line(len(text)+8)
            try:
                option = int(input('Digite uma opção: '))
                if option in valid_range:
                    return option

                self.terminal.clear()
                self.printer.error('Opção inválida. Tente novamente.')

            except ValueError:
                self.terminal.clear()
                self.printer.error('Por favor, digite um número válido.')

    def invalid_option(self):
        self.terminal.clear()
        self.printer.error('Opção inválida, tente novamente')
        self.terminal.clear()

    def invalid_value(self):
        self.terminal.clear()
        self.printer.error('Valor inválido, tente novamente')
        self.terminal.clear()
