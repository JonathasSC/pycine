from pydantic import BaseModel
from typing import Optional


class SessionBase(BaseModel):
    session_id: str


class SessionCreate(SessionBase):
    price: str
    room_id: str
    movie_id: str
    start_time: str


class SessionUpdate(BaseModel):
    price: Optional[str]
    room_id: Optional[str]
    movie_id: Optional[str]
    start_time: Optional[str]
