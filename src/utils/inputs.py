class Inputs:
    def __init__(self) -> None:
        pass

    def input_person(self):
        person_data: dict = {}

        person_data['name'] = input('Nome: ')
        person_data['email'] = input('Email: ')
        person_data['password'] = input('Senha: ')

        return person_data

    def input_movie(self):
        movie_data: dict = {}

        movie_data['name'] = input('Nome: ')
        movie_data['duration'] = input('Duration: ')
        movie_data['synopsis'] = input('Synopsis: ')

        return movie_data