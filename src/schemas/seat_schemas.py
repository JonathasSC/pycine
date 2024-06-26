from pydantic import BaseModel, field_validator
from typing import Literal


class SeatBase(BaseModel):
    seat_id: str

    @field_validator('seat_id')
    def validate_room_id(cls, value: str):
        if not value.strip():
            raise ValueError('Seat ID must not be empty.')

        return value


class SeatCreate(SeatBase):
    room_id: str
    line: str
    column: str
    state: Literal['reserved', 'sold', 'available']

    @field_validator('room_id')
    def validate_room_id(cls, value: str):
        if not value.strip():
            raise ValueError('Room ID must not be empty.')

        return value

    @field_validator('line')
    def validate_line(cls, value: str):
        if not value.strip():
            raise ValueError('Line must not be empty.')

        return value

    @field_validator('column')
    def validate_column(cls, value: str):
        if not value.strip():
            raise ValueError('Column must not be empty.')

        return value

    @field_validator('state')
    def validate_state(cls, value: str):
        valid_states = {'reserved', 'sold', 'available'}
        if value not in valid_states:
            raise ValueError(f'State must be one of {valid_states}')

        return value
