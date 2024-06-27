from pydantic import BaseModel, field_validator
from typing import Optional


class MovieBase(BaseModel):
    movie_id: str


class MovieCreate(MovieBase):
    name: str
    genre: str
    duration: str
    synopsis: Optional[str]

    @field_validator('name')
    def validate_name(cls, value: str):
        if not value.strip():
            raise ValueError('Name must not be empty.')

        if len(value) < 2:
            raise ValueError('Name must be at least 2 characters long.')

        return value

    @field_validator('synopsis')
    def validate_name(cls, value: str):
        if not value.strip():
            raise ValueError('Synopsis must not be empty.')

        if len(value) < 2:
            raise ValueError('Synopsis must be at least 2 characters long.')

        return value
