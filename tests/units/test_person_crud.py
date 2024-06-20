import os
import pytest
from faker import Faker

from src.database.conn import Connection
from src.crud.persons_crud import PersonsCrud
from src.utils.uuid import UUID


class TestPersonCrud:

    # Config Teardown
    @pytest.fixture(autouse=True)
    def setup_teardown(self):
        self.db_name = 'test.db'
        self.conn: Connection = Connection(self.db_name)
        self.conn.connect()

        yield

        self.conn.close()

        if os.path.exists(self.db_name):
            os.remove(self.db_name)

    @pytest.fixture(scope='class')
    def test_data(self):
        faker = Faker()

        test_email = faker.email()
        test_password = faker.password()
        test_name = f'{faker.name()} {Faker().last_name()}'

        return {
            "name": test_name,
            "email": test_email,
            "password": test_password,
        }

    def test_insert_person(self, test_data):
        crud: PersonsCrud = PersonsCrud(self.conn)
        is_created = crud.insert_person(test_data)
        assert is_created is True

    def test_select_person_by_email(self, test_data):
        crud: PersonsCrud = PersonsCrud(self.conn)
        crud.insert_person(test_data)
        
        person = crud.select_person_by_email(test_data['email'])
        assert isinstance(person, tuple)
