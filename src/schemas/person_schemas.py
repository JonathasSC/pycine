from pydantic import BaseModel, EmailStr, field_validator
from typing import Optional
import re


class PersonCreate(BaseModel):
    name: str
    email: EmailStr
    password: str

    @field_validator('password')
    def validate_password(cls, value: str):
        if len(value) < 8:
            raise ValueError('Password must be at least 8 characters long.')

        if not re.search(r'[A-Z]', value):
            raise ValueError(
                'Password must contain at least one uppercase letter.')

        if not re.search(r'[a-z]', value):
            raise ValueError(
                'Password must contain at least one lowercase letter.')

        if not re.search(r'[0-9]', value):
            raise ValueError('Password must contain at least one digit.')

        if not re.search(r'[!_@#$%^&*()+,.?":{}|<>]', value):
            raise ValueError(
                'Password must contain at least one special character.')

        return value

    @field_validator('name')
    def validate_name(cls, value: str):
        if not value.strip():
            raise ValueError('Name must not be empty.')

        if len(value) < 2:
            raise ValueError('Name must be at least 2 characters long.')

        if not re.match(r'^[.a-zA-Z\s]+$', value):
            raise ValueError(
                'Name must contain only alphabetic characters and spaces.')

        return value
