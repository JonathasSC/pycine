# sessions_queries.py
CREATE_SESSION_TABLE = """
CREATE TABLE IF NOT EXISTS sessions (
    session_id TEXT PRIMARY KEY,
    
    room_id TEXT,
    movie_id TEXT,

    price TEXT,
    start_time TEXT,

    FOREIGN KEY (room_id) REFERENCES rooms(room_id)
);
"""

SELECT_ALL_SESSIONS = """
SELECT session_id, price, room_id, movie_id, start_time
FROM sessions;
"""


SELECT_SESSIONS_BY_MOVIE_ID = """
SELECT session_id, price, room_id, movie_id, start_time
FROM sessions WHERE movie_id = ?;
"""

INSERT_SESSION = """
INSERT INTO sessions (session_id, price, room_id, movie_id, start_time)
VALUES (?, ?, ?, ?, ?);
"""

UPDATE_SESSION = """
UPDATE sessions
SET price = ?, room_id = ?, movie_id = ?, start_time = ?
WHERE session_id = ?;
"""

DELETE_SESSION = """
DELETE FROM sessions
WHERE session_id = ?;
"""
