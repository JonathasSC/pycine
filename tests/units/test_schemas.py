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
        test_data: dict = {}

        test_data['person_id'] = UUID().smaller_uuid()
        test_data['name'] = f'{faker.name()} {Faker().last_name()}'
        test_data['email'] = faker.email()
        test_data['password'] = faker.password()

        return test_data

    @pytest.fixture(scope='class')
    def invalid_data(self):
        test_fail_data: dict = {}

        test_fail_data['person_id'] = 'invalid_uuid'
        test_fail_data['name'] = 123
        test_fail_data['email'] = 'invalid_email'
        test_fail_data['password'] = ''

        return test_fail_data

    def test_valid_person(self, test_data):
        person = PersonCreate(**test_data)
        assert isinstance(person, PersonCreate)

    def test_invalid_person_data(self, invalid_data):
        with pytest.raises(ValidationError):
            PersonCreate(**invalid_data)


if __name__ == '__main__':
    pytest.main()
