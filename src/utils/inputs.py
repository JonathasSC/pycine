from src.utils.printer import Printer
from src.utils.terminal import Terminal
import getpass
from typing import Optional, Dict
from src.utils.validators import password_validator
from datetime import datetime
import re


class Inputs:
    def __init__(self) -> None:
        self.printer: Printer = Printer()
        self.terminal: Terminal = Terminal()

    def input_login(self) -> Dict[str, str]:
        person_data: dict = {}

        person_data['email'] = input('Email: ')
        person_data['password'] = input('Senha: ')

        return person_data

    def input_person(self) -> Optional[Dict[str, str]]:
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

    def input_register(self) -> Dict[str, str]:
        person_data: dict = {}

        person_data['name'] = input('Nome: ')
        person_data['email'] = input('Email: ')
        person_data['password'] = self.input_password()

        return person_data

    def input_password(self) -> Dict[str, str]:
        while True:
            password = getpass.getpass('Senha (ela está ocultada): ')
            confirm_password: str = getpass.getpass('Confirme a senha: ')

            if password != confirm_password:
                self.printer.error('Senhas não correspondem, tente novamente')
                pass

            elif not password_validator(password):
                self.terminal.clear()
                self.printer.password_params()

            else:
                return password

    def input_movie(self) -> Optional[dict]:
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

    def input_seat(self) -> Optional[dict]:
        ticket_data: dict = {}
        ticket_data['Room ID'] = input('')

    def input_room(self) -> Optional[dict]:
        room_data: dict = {}

        room_data['name'] = input('Name: ')
        if room_data['name'] == 'q':
            return None

        room_data['rows'] = int(input('Rows: '))
        if room_data['rows'] == 'q':
            return None

        room_data['columns'] = int(input('Columns: '))
        if room_data['columns'] == 'q':
            return None

        valid_types = ['normal', 'dubbed', 'subtitled', 'vip']
        self.terminal.clear()

        option: int = self.choose_an_option(
            valid_types,
            'Escolha o tipo da sala:',
            cancel=True
        )

        if option == 0:
            return None

        room_data['type'] = valid_types[option - 1]
        return room_data

    def input_session(self) -> Optional[dict]:
        session_data: dict = {}

        session_data['price'] = self.input_price('Price (00.00): ')
        if session_data['price'] is None:
            return None

        session_data['room_id'] = input('Room ID: ')
        if session_data['room_id'] == 'q':
            return None

        session_data['movie_id'] = input('Movie ID: ')
        if session_data['movie_id'] == 'q':
            return None

        session_data['start_date'] = self.input_date(
            'Start date (dd/mm/yyyy)')
        if session_data['start_date'] is None:
            return None

        session_data['start_time'] = self.input_time(
            'Start time (HH:MM)')
        if session_data['start_time'] is None:
            return None

        return session_data

    def choose_an_option(self,
                         options: list,
                         text: str = 'Escolha uma opção',
                         cancel: bool = False,
                         clear: bool = True):

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
        self.printer.error('Opção inválida, tente novamente', clear=True)

    def invalid_value(self):
        self.printer.error('Valor inválido, tente novamente', clear=True)

    def input_date(self, prompt: str) -> Optional[str]:
        while True:
            date_input = input(prompt)
            if date_input.lower() == 'q':
                return None
            try:
                parsed_date = datetime.strptime(date_input, '%d/%m/%Y').date()
                return parsed_date.isoformat()

            except ValueError:
                self.printer.error(
                    text="Formato de data inválido. Use o formato dd/mm/aaaa.",
                    clear=True)

    def input_time(self, prompt: str) -> Optional[str]:
        while True:
            time_input = input(prompt)
            if time_input.lower() == 'q':
                return None
            try:
                parsed_time = datetime.strptime(time_input, '%H:%M').time()
                return parsed_time.strftime('%H:%M')

            except ValueError:
                self.printer.error(
                    text="Formato de hora inválido. Use o formato HH:MM.",
                    clear=True)

    def input_price(self, prompt: str) -> Optional[str]:
        while True:
            regex = r'^\d+(?:\.\d{2})?$'
            price = input(prompt).strip()

            if price.lower() == 'q':
                return None

            if re.match(regex, price):
                return price

            self.printer.error(
                text="Formato de preço inválido. Insira um numéro válido e positivo.",
                clear=True)
