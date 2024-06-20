CREATE_ROOMS_TABLE = """
CREATE TABLE IF NOT EXISTS rooms (
    room_id INTEGER PRIMARY KEY,
    name VARCHAR(10),
    rows INTEGER,
    columns INTEGER,
    type VARCHAR(25) CHECK (type in ('normal', 'dubbed', 'subtitled', 'vip'))
);
"""

INSERT_ROOM = """
INSERT INTO rooms (name, type, front_seats, middle_seats, back_seats)
VALUES (?, ?, ?, ?, ?);
"""

SELECT_ROOM_BY_ID = """
SELECT * FROM rooms WHERE room_id = ?;
"""

SELECT_ROOM_BY_TYPE = """
SELECT * FROM rooms WHERE type = ?;
"""

UPDATE_ROOM = """
UPDATE rooms
SET front_seats = ?, middle_seats = ?, back_seats = ?
WHERE room_id = ?;
"""

DELETE_ROOM = """
DELETE FROM rooms WHERE room_id = ?;
"""
