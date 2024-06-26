from pydantic import BaseModel, field_validator


class RoomBase(BaseModel):
    room_id: str


class RoomCreate(RoomBase):
    name: str
    rows: int
    columns: int
    type: str

    @field_validator('name')
    def validate_name(cls, value: str):
        if not value.strip():
            raise ValueError('Name must not be empty.')

        if len(value) < 2:
            raise ValueError('Name must be at least 2 characters long.')

        return value

    @field_validator('rows')
    def validate_rows(cls, value: int):
        if value <= 0:
            raise ValueError('Rows must be a positive integer.')

        return value

    @field_validator('columns')
    def validate_columns(cls, value: int):
        if value <= 0:
            raise ValueError('Columns must be a positive integer.')

        return value

    @field_validator('type')
    def validate_type(cls, value: str):
        if not value.strip():
            raise ValueError('Type must not be empty.')

        return value
