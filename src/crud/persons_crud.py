from typing import Any, Dict, List, Optional, Union
from src.crud.base_crud import BaseCrud


from src.queries.persons_queries import (
    INSERT_PERSON,
    SELECT_BY_EMAIL,
    DELETE_ALL_PERSONS,
    SELECT_IS_ADMIN,
    SELECT_IS_CLIENT
)

from src.schemas.person_schemas import PersonCreate, PersonLogin
from pydantic import ValidationError


class PersonsCrud(BaseCrud):
    def __init__(self):
        super().__init__()

    def insert_person(self, data: Dict[str, Any]) -> bool:
        try:
            person_id: str = self.uuid.smaller_uuid()
            data['password'] = self.hash.generate_hash(data['password'])
            data['person_id'] = person_id

            data_dict: Dict[str, Any] = dict(PersonCreate(**data))
            data_list: List[Any] = list(data_dict.values())

            self.conn.cursor.execute(INSERT_PERSON, data_list)
            self.conn.connection.commit()

            return True

        except ValidationError as e:
            print(f"Validation error: {e}")
            return False

        except Exception as e:
            print(f"Error inserting person: {e}")
            return False

    def select_by_credentials(self, data: Dict[str, str]) -> Union[tuple, bool, Exception]:
        try:
            data_dict: Dict[str, Any] = dict(PersonLogin(**data))

            person_email: str = data_dict['email']
            person_unhashed_password: str = data_dict['password']
            self.conn.cursor.execute(SELECT_BY_EMAIL, [person_email])
            person: Optional[tuple] = self.conn.cursor.fetchone()

        except ValidationError as e:
            raise e

        except Exception as e:
            raise e

        person_hashed_password: str = person[3]
        if person and self.hash.verify_hash(person_unhashed_password, person_hashed_password):
            return person

    def select_by_email(self, email: str) -> Optional[tuple]:
        try:
            self.conn.cursor.execute(SELECT_BY_EMAIL, [email])
            person: Optional[tuple] = self.conn.cursor.fetchone()
            return person
        except Exception as e:
            raise e

    def delete_all_persons(self):
        try:
            self.conn.cursor.execute(DELETE_ALL_PERSONS)
            self.conn.connection.commit()
            return True
        except Exception as e:
            raise e

    def get_person_role(self, person_id: str):
        self.conn.cursor.execute(SELECT_IS_ADMIN, [person_id])
        if self.conn.cursor.fetchone():
            return 'admin'

        self.conn.cursor.execute(SELECT_IS_CLIENT, [person_id])
        if self.conn.cursor.fetchone():
            return 'client'

        return None
