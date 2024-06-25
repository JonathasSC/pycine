import pytest
from faker import Faker

from src.database.conn import Connection
from src.crud.persons_crud import PersonsCrud


class TestPersonCrud:
    @pytest.fixture(autouse=True)
    def setup_teardown(self):
        self.db_name = 'test.db'
        self.conn: Connection = Connection(self.db_name)
        self.conn.connect()

    @pytest.fixture(scope='class')
    def test_data(self):
        faker = Faker()

        test_data: dict = {}

        test_data['name'] = f'{faker.name()} {Faker().last_name()}'
        test_data['email'] = faker.email()
        test_data['password'] = faker.password()

        return test_data

    def test_insert_person(self, test_data: dict):
        crud: PersonsCrud = PersonsCrud(self.conn)
        is_created = crud.insert_person(test_data)
        assert is_created is True

    def test_select_by_email(self, test_data: dict):
        crud: PersonsCrud = PersonsCrud(self.conn)
        crud.insert_person(test_data)

        person = crud.select_by_email(test_data['email'])
        assert person is not None
