import re


def password_validator(senha: str):
    padrao = r'^(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%^&*()-_+=])[A-Za-z\d!@#$%^&*()-_+=]{8,}$'

    if re.match(padrao, senha):
        return True
    else:
        return False
