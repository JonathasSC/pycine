import re
import getpass
from datetime import datetime
from typing import Optional, Dict

from src.utils.printer import Printer
from src.utils.terminal import Terminal

from src.utils.validators import (
    exists_room,
    email_validator,
    password_validator,
    exists_room_by_name,
)


class Inputs:
    def __init__(self) -> None:
        self.printer: Printer = Printer()
        self.terminal: Terminal = Terminal()

    def input_login(self) -> Optional[dict]:
        person_data: dict = {}

        person_data['email'] = input('Email: ')
        if person_data['email'] == 'q':
            return None

        person_data['password'] = input('Senha: ')
        if person_data['password'] == 'q':
            return None

        return person_data

    def input_person(self) -> Optional[Dict[str, str]]:
        person_data: dict = {}

        person_data['name'] = input('Nome: ')
        if person_data['name'] == 'q':
            return None

        person_data['email'] = self.input_email('Email: ')
        if person_data['email'] == None:
            return None

        person_data['password'] = self.input_password('Senha: ')
        if person_data['password'] == None:
            return None

        return person_data

    def input_register(self) -> Optional[dict]:
        person_data: dict = {}

        person_data['name'] = input('Nome: ').strip()
        if person_data['name'] in 'Qq':
            return None

        person_data['email'] = self.input_email('Email: ')
        if person_data['email'] == None:
            return None

        person_data['password'] = self.input_password(
            'Senha (ela está ocultada): ')
        if person_data['password'] == None:
            return None

        return person_data

    def input_movie(self) -> Optional[dict]:
        movie_data: dict = {}

        movie_data['name'] = input('Nome: ').strip().lower()
        if movie_data['name'] == 'q':
            return None

        movie_data['genre'] = input('Genre: ').strip().lower()
        if movie_data['genre'] == 'q':
            return None

        movie_data['duration'] = self.input_time('Duration (HH:MM):')
        if movie_data['duration'] == 'q':
            return None

        movie_data['synopsis'] = input('Synopsis: ').strip().lower()
        if movie_data['synopsis'] == 'q':
            return None

        return movie_data

    def get_integer_input(self, prompt):
        while True:
            user_input = input(prompt)
            if user_input == 'q':
                return None
            if user_input.isdigit():
                return int(user_input)
            self.printer.error('Preencha com um número válido', clear=True)

    def input_room(self) -> Optional[dict]:
        room_data: dict = {}

        room_data['name'] = input('Nome da sala: ').strip().lower()
        if room_data['name'] == 'q':
            return None

        while room_data['name'] and not exists_room_by_name(room_data['name']):
            self.printer.error('Nome invalido ou já em uso.', clear=True)
            room_data['name'] = input(
                'Nome da sala (deixe em branco para manter o atual): ').strip().lower()
            if room_data['name'] == 'q':
                return None

        room_data['rows'] = self.get_integer_input('Linhas: ')
        if room_data['rows'] is None:
            return None

        room_data['columns'] = self.get_integer_input('Colunas: ')
        if room_data['columns'] is None:
            return None

        options = ['normal', 'dublado', 'legendado', 'vip']
        valid_types = ['normal', 'dubbed', 'subtitled', 'vip']
        self.terminal.clear()

        option: int = self.choose_an_option(
            options,
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
        if session_data['price'] == None:
            return None

        session_data['room_id'] = self.input_room_id('Room ID: ')
        if session_data['room_id'] == None:
            return None

        session_data['movie_id'] = input('Movie ID: ')
        if session_data['movie_id'] == 'q':
            return None

        session_data['start_date'] = self.input_date(
            'Start date (dd/mm/yyyy): ')
        if session_data['start_date'] is None:
            return None

        session_data['start_time'] = self.input_time(
            'Start time (HH:MM): ')
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

    def input_email(self, prompt: str) -> Optional[str]:
        while True:
            email = input(prompt).strip()
            if email.lower() == 'q':
                return None

            if email_validator(email):
                return email

            self.printer.error(
                text="Esse email não é valido ou está indisponivel",
                clear=True)

    def input_password(self, prompt) -> Optional[str]:
        while True:
            password = getpass.getpass(prompt)
            if password.lower() == 'q':
                return None

            confirm_password = getpass.getpass(
                'Confirme (ela está ocultada): ')
            if confirm_password.lower() == 'q':
                return None

            if password != confirm_password:
                self.printer.error('Senhas não correspondem, tente novamente')
                continue

            if password_validator(password):
                return password

            self.terminal.clear()
            self.printer.password_params()

    def input_room_id(self, prompt: str) -> Optional[str]:
        while True:
            room_id = input(prompt).strip()
            if room_id.lower() == 'q':
                return None

            if not exists_room(room_id):
                return room_id

            self.printer.error(
                text='Nenhuma sala identificada tente novamente',
                clear=True)

    def input_movie(self) -> None:
        movie_data: dict = {}

        movie_data['name'] = input(
            'Nome (deixe em branco para manter o atual): ').strip().lower()
        if movie_data['name'] == 'q':
            return None

        movie_data['genre'] = input(
            'Genre (deixe em branco para manter o atual): ').strip().lower()
        if movie_data['genre'] == 'q':
            return None

        while True:
            movie_data['duration'] = input(
                'Duration (HH:MM) (deixe em branco para manter o atual): ').strip().lower()
            if movie_data['duration'] == 'q':
                return None
            elif movie_data['duration'] == '':
                break
            else:
                try:
                    formated_duration = datetime.strptime(
                        movie_data['duration'], '%H:%M').time()
                    movie_data['duration'] = formated_duration
                    break
                except ValueError:
                    self.printer.error(
                        text="Formato de hora inválido. Use o formato HH:MM.",
                        clear=True)

        movie_data['synopsis'] = input(
            'Synopsis (deixe em branco para manter o atual): ').strip().lower()
        if movie_data['synopsis'] == 'q':
            return None

        return movie_data

    def input_put_room(self) -> None:
        room_data: dict = {}

        room_data['name'] = input(
            'Nome da sala (deixe em branco para manter o atual): ').strip().lower()
        if room_data['name'] == 'q':
            return None

        while room_data['name'] and not exists_room_by_name(room_data['name']):
            self.printer.error('Nome invalido ou já em uso.', clear=True)
            room_data['name'] = input(
                'Nome da sala (deixe em branco para manter o atual): ').strip().lower()
            if room_data['name'] == 'q':
                return None

        room_data['rows'] = self.get_integer_input(
            'Linhas (deixe em branco para manter o atual): ')
        if room_data['rows'] is None:
            return None

        room_data['columns'] = self.get_integer_input(
            'Colunas (deixe em branco para manter o atual): ')
        if room_data['columns'] is None:
            return None

        options = ['normal', 'dublado', 'legendado', 'vip']
        valid_types = ['normal', 'dubbed', 'subtitled', 'vip']
        self.terminal.clear()

        option: int = self.choose_an_option(
            options,
            'Escolha o tipo da sala:',
            cancel=True
        )

        if option == 0:
            return None

        room_data['type'] = valid_types[option - 1]

        return room_data

    def input_put_person(self) -> None:
        person_data: dict = {}

        person_data['name'] = input(
            'Nome (deixe em branco para manter o atual): ').strip()
        if person_data['name'] == 'q':
            return None

        person_data['email'] = input(
            'Email (deixe em branco para manter o atual): ').strip()
        if person_data['email'] == 'q':
            return None

        while person_data['email'] and not email_validator(person_data['email']):
            self.printer.error('Email invalido ou já em uso.', clear=True)
            person_data['email'] = input('Email: ')
            if person_data['email'] == 'q':
                return None

        person_data['password'] = input(
            'Senha (deixe em branco para manter a atual): ').strip()
        if person_data['password'] == 'q':
            return None

        while person_data['password'] and not password_validator(person_data['password']):
            self.terminal.clear()
            self.printer.password_params()
            self.terminal.clear()

            person_data['password'] = input('Senha: ').strip()
            if person_data['password'] == 'q':
                return None

        return person_data
