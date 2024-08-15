import re
from src.queries.persons_queries import SELECT_BY_EMAIL
from src.queries.sessions_queries import SELECT_BY_ROOM_START_DATE_AND_TIME
from src.queries.rooms_queries import SELECT_ROOM_BY_ID, SELECT_ROOM_BY_NAME
from src.queries.movies_queries import SELECT_MOVIE_BY_NAME, SELECT_MOVIE_BY_ID
from src.database.conn import Connection


def password_validator(senha: str) -> bool:
    padrao = r'^(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%^&*()-_+=])[A-Za-z\d!@#$%^&*()-_+=]{8,}$'

    return re.match(padrao, senha)


def exists_email(email: str) -> bool:
    conn: Connection = Connection(auto_connect=False)

    conn.connect()
    conn.cursor.execute(SELECT_BY_EMAIL, [email])
    person_exists: tuple = conn.cursor.fetchone()
    conn.close()

    return person_exists is None


def validate_seat_choice(seats, chosen_seat):
    for seat in seats:
        if seat[2] == chosen_seat.upper():
            return seat[5] if seat[5] == 'available' else None
    return None


def email_validator(email: str) -> bool:
    regex = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    if not exists_email(email):
        return False

    if not re.match(regex, email):
        return False

    return True


def exists_session(room_id: str, start_date: str, start_time: str) -> bool:
    conn: Connection = Connection(auto_connect=False)

    conn.connect()
    conn.cursor.execute(SELECT_BY_ROOM_START_DATE_AND_TIME,
                        [room_id, start_date, start_time])
    session_exists: tuple = conn.cursor.fetchone()
    conn.close()

    return session_exists is None


def exists_movie_by_id(movie_id: str):
    conn: Connection = Connection(auto_connect=False)

    conn.connect()
    conn.cursor.execute(SELECT_MOVIE_BY_ID, [movie_id])
    exists: tuple = conn.cursor.fetchone()
    conn.close()

    return exists is None


def exists_movie_by_name(name: str):
    conn: Connection = Connection(auto_connect=False)

    conn.connect()
    conn.cursor.execute(SELECT_MOVIE_BY_NAME, [name])
    exists: tuple = conn.cursor.fetchone()
    conn.close()

    return exists is None


def exists_room_by_id(room_id: str):
    conn: Connection = Connection(auto_connect=False)

    conn.connect()
    conn.cursor.execute(SELECT_ROOM_BY_ID, [room_id])
    exists: tuple = conn.cursor.fetchone()
    conn.close()

    return exists is None


def exists_room_by_name(name: str):
    conn: Connection = Connection(auto_connect=False)

    conn.connect()
    conn.cursor.execute(SELECT_ROOM_BY_NAME, [name])
    exists: tuple = conn.cursor.fetchone()
    conn.close()

    return exists is None


def price_validator(price: str):
    regex = r'^\d+(?:\.\d{2})?$'
    return re.match(regex, price)
