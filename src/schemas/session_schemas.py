from typing import Optional
from datetime import date, time
from pydantic import BaseModel


class SessionBase(BaseModel):
    session_id: str


class SessionCreate(SessionBase):
    room_id: str
    movie_id: str
    price: str
    start_time: time
    start_date: date


class SessionUpdate(BaseModel):
    price: Optional[float]
    room_id: Optional[str]
    movie_id: Optional[str]
    start_time: Optional[time]
    start_date: Optional[date]
