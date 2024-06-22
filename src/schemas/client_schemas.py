from pydantic import BaseModel


class ClientBase(BaseModel):
    client_id: str


class PersonCreate(ClientBase):
    person_id: str
