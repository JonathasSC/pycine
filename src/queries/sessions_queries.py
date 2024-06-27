# sessions_queries.py

SELECT_ALL_SESSIONS = """
SELECT session_id, price, room_id, movie_id, start_time
FROM sessions;
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
