from src.crud.base_crud import BaseCrud
from src.database.conn import Connection

from typing import (
    Any,
    Dict, 
    List, 
    Optional,
    Union
)


from src.queries.persons_queries import (
    INSERT_PERSON,
    SELECT_BY_EMAIL,
    DELETE_ALL_PERSONS,
    SELECT_IS_ADMIN,
    SELECT_IS_CLIENT,
    SELECT_ALL_PERSONS,
    DELETE_PERSON_BY_ID,
    SELECT_PERSON_BY_ID
)

from src.schemas.person_schemas import PersonCreate, PersonLogin
from pydantic import ValidationError


class PersonsCrud(BaseCrud):
    def __init__(self, conn: Connection = None):
        super().__init__(conn)

    def insert_person(self, data: Dict[str, Any]) -> bool:
        try:
            person_id: str = self.uuid.smaller_uuid()
            data['person_id'] = person_id
            data['password'] = self.hash.generate_hash(data['password'])

            data_dict: Dict[str, Any] = dict(PersonCreate(**data))

            data_list: List[Any] = list(data_dict.values())

            self.conn.connect()
            self.conn.cursor.execute(INSERT_PERSON, data_list)
            self.conn.connection.commit()
            self.conn.close()

            return person_id

        except ValidationError as e:
            raise e

        except Exception as e:
            raise e

    def select_by_credentials(self, data: Dict[str, str]) -> Union[tuple, None]:
        try:
            data_dict: PersonLogin = PersonLogin(**data)

            person_email: str = data_dict.email
            person_unhashed_password: str = data_dict.password
            
            self.conn.connect()
            self.conn.cursor.execute(SELECT_BY_EMAIL, [person_email])
            person: Optional[tuple] = self.conn.cursor.fetchone()
            self.conn.close()

            if person:
                person_hashed_password: str = person[3]
                is_valid_password: bool = self.hash.verify_hash(
                    person_unhashed_password,
                    person_hashed_password
                )

                if is_valid_password:
                    return person

            return None

        except ValidationError as e:
            raise e

        except Exception as e:
            raise e

    def select_all_clients(self) -> list:
        try:
            self.conn.connect()
            self.conn.cursor.execute(SELECT_ALL_PERSONS)
            person_list: list = self.conn.cursor.fetchall()
            self.conn.close()
            return person_list

        except Exception as e:
            raise e

    def select_by_id(self, person_id: str) -> Optional[tuple]:
        try:
            self.conn.connect()
            self.conn.cursor.execute(SELECT_PERSON_BY_ID, [person_id])
            person: Optional[tuple] = self.conn.cursor.fetchone()
            self.conn.close()
            return person

        except Exception as e:
            raise e

    def select_by_email(self, email: str) -> Optional[tuple]:
        try:
            self.conn.connect()
            self.conn.cursor.execute(SELECT_BY_EMAIL, [email])
            person: Optional[tuple] = self.conn.cursor.fetchone()
            self.conn.close()
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

    def get_person_role(self, person_id: str) -> Optional[str]:
        try:
            self.conn.cursor.execute(SELECT_IS_ADMIN, [person_id])
            if self.conn.cursor.fetchone():
                return 'admin'

            self.conn.cursor.execute(SELECT_IS_CLIENT, [person_id])
            if self.conn.cursor.fetchone():
                return 'client'

            return None
        except Exception as e:
            print(f"Erro ao pegar papel de pessoa: {e}")
            return None

    def delete_person(self, person_id: str):
        try:
            self.conn.connect()
            self.conn.cursor.execute(DELETE_PERSON_BY_ID, [person_id])
            self.conn.connection.commit()
            self.conn.close()

            return person_id
        except Exception as e:
            print(f"Erro ao deletar pessoa: {e}")
            return None
