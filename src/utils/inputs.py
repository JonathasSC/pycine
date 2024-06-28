class Inputs:
    def __init__(self) -> None:
        pass

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
        room_data: dict = {}

        room_data['name'] = input('Nome: ')
        room_data['rows'] = int(input('Rows: '))
        room_data['columns'] = int(input('Columns: '))
        room_data['type'] = input('Type: ')

        return room_data

    def input_session(self):
        session_data: dict = {}

        session_data['room_id'] = input('Room ID: ')
        session_data['movie_id'] = input('Movie ID: ')
        session_data['price'] = input('Price: ')
        session_data['start_time'] = input('Start time: ')

        return session_data
