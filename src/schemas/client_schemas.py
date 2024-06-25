from pydantic import BaseModel


class ClientBase(BaseModel):
    client_id: str


class ClientCreate(ClientBase):
    person_id: str
