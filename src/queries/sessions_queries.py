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

SELECT_SESSIONS_WITH_ROOM_DETAILS = '''
SELECT 
    s.price,
    s.start_time,
    r.type AS room_type,
    r.name AS room_name,
    m.name AS movie_name
FROM 
    sessions s
JOIN 
    rooms r ON s.room_id = r.room_id
JOIN 
    movies m ON s.movie_id = m.movie_id
WHERE 
    s.movie_id = ?;
'''

SELECT_ALL_SESSIONS_WITH_MOVIES = '''
SELECT 
    m.name AS movie_name,
    m.genre AS movie_genre,
    m.duration AS movie_duration,
    m.synopsis AS movie_synopsis,
    s.movie_id AS session_movie_id,
    s.session_id AS session_id,
    s.room_id AS session_room_id
FROM sessions s
JOIN movies m ON s.movie_id = m.movie_id;
'''


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

DELETE_ALL_SESSIONS = """
DELETE FROM sessions
"""
