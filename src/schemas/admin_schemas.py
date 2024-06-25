from pydantic import BaseModel


class AdminBase(BaseModel):
    admin_id: str


class AdminCreate(AdminBase):
    person_id: str
