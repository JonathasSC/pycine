CREATE_ROOMS_TABLE = """
CREATE TABLE IF NOT EXISTS rooms (
    room_id TEXT PRIMARY KEY,
    name TEXT,
    rows INTEGER,
    columns INTEGER,
    type TEXT CHECK (type in ('normal', 'dubbed', 'subtitled', 'vip'))
);
"""

INSERT_ROOM = """
INSERT INTO rooms (room_id, name, rows, columns, type)
VALUES (?, ?, ?, ?, ?);
"""

SELECT_ROOM_BY_ID = """
SELECT * FROM rooms WHERE room_id = ?;
"""

SELECT_ROOM_BY_TYPE = """
SELECT * FROM rooms WHERE type = ?;
"""

SELECT_ALL_ROOMS = """
SELECT * FROM rooms;
"""

UPDATE_ROOM = """
UPDATE rooms
SET name TEXT = ?, rows = ?, columns = ?, type = ?
WHERE room_id = ?;
"""

DELETE_ROOM = """
DELETE FROM rooms WHERE room_id = ?;
"""
