from pydantic import BaseModel, field_validator
from typing import Optional
from datetime import date, time
from decimal import Decimal


class SessionBase(BaseModel):
    session_id: str


class SessionCreate(SessionBase):
    room_id: str
    movie_id: str
    price: Decimal
    start_time: time
    start_date: date

    @field_validator('price')
    def validate_price(cls, value):
        if value < 0:
            raise ValueError('O preço deve ser um valor positivo')
        return value


class SessionUpdate(BaseModel):
    price: Optional[Decimal]
    room_id: Optional[str]
    movie_id: Optional[str]
    start_time: Optional[time]
    start_date: Optional[date]

    @field_validator('price')
    def validate_price(cls, value):
        if value < 0:
            raise ValueError('Price must be a positive value')
        return value
