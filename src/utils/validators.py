import re
from src.queries.persons_queries import SELECT_BY_EMAIL
from src.database.conn import Connection


def password_validator(senha: str):
    padrao = r'^(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%^&*()-_+=])[A-Za-z\d!@#$%^&*()-_+=]{8,}$'

    if re.match(padrao, senha):
        return True
    return False


def exists_email(email: str):
    conn: Connection = Connection(auto_connect=False)

    conn.connect()
    conn.cursor.execute(SELECT_BY_EMAIL, [email])
    person_exists: tuple = conn.cursor.fetchone()
    conn.close()

    if person_exists:
        return False
    return True


def validate_seat_choice(seats, chosen_seat):
    for seat in seats:
        if seat[2] == chosen_seat:
            if seat[5] == 'available':
                return seat[5]
            return None
    return None
