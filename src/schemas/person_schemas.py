from pydantic import BaseModel, field_validator
import re


class PersonBase(BaseModel):
    person_id: str


class PersonCreate(PersonBase):
    name: str
    email: str
    password: str

    @field_validator('password')
    def validate_password(cls, value: str):
        if len(value) < 8:
            raise ValueError('A senha deve ter pelo menos 8 caracteres.')

        if not re.search(r'[A-Z]', value):
            raise ValueError(
                'A senha deve conter pelo menos uma letra maiúscula.')

        if not re.search(r'[a-z]', value):
            raise ValueError(
                'A senha deve conter pelo menos uma letra minúscula.')

        if not re.search(r'[0-9]', value):
            raise ValueError('A senha deve conter pelo menos um dígito.')

        if not re.search(r'[!_@#$%^&*()+,.?":{}|<>]', value):
            raise ValueError(
                'A senha deve conter pelo menos um caractere especial.')

        return value

    @field_validator('email')
    def validate_email(cls, value):
        if not re.match(r"[^@]+@[^@]+\.[^@]+", value):
            raise ValueError('Endereço de email inválido.')

        return value

    @field_validator('name')
    def validate_name(cls, value: str):
        if not value.strip():
            raise ValueError('O nome não pode estar vazio.')

        if len(value) < 2:
            raise ValueError('O nome deve ter pelo menos 2 caracteres.')

        if not re.match(r'^[.a-zA-Z\s]+$', value):
            raise ValueError(
                'O nome deve conter apenas caracteres alfabéticos e espaços.')

        return value


class PersonLogin(BaseModel):
    email: str
    password: str
