# test_person_schemas.py
import pytest
from src.schemas.person_schemas import PersonCreate
from pydantic import ValidationError
from src.utils.uuid import UUID
from faker import Faker


class TestPersonCreate:

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

    @pytest.fixture(scope='class')
    def invalid_data(self):
        return {
            "name": 123,
            "email": "invalid_email",
            "password": "",
        }

    def test_valid_person(self, test_data):
        person = PersonCreate(**test_data)
        assert isinstance(person, PersonCreate)

    def test_invalid_person_data(self, invalid_data):
        with pytest.raises(ValidationError):
            PersonCreate(**invalid_data)


if __name__ == '__main__':
    pytest.main()
