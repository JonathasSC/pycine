CREATE_SEATS_TABLE = """
CREATE TABLE IF NOT EXISTS seats (
    seat_id TEXT PRIMARY KEY,
    room_id TEXT,
    seat_code TEXT,
    row INTEGER,
    col INTEGER,
    state TEXT CHECK (state IN ('reserved', 'sold', 'available')),
    FOREIGN KEY (room_id) REFERENCES rooms(room_id) ON DELETE CASCADE
);
"""

DELETE_SEATS_TABLE = """
DROP TABLE IF EXISTS seats;
"""


INSERT_SEAT = """
INSERT INTO seats (seat_id, room_id, seat_code, row, col, state)
    VALUES (?, ?, ?, ?, ?, ?)
"""


SELECT_SEAT_BY_ID = """
SELECT * FROM seats WHERE seat_id = ?;
"""

SELECT_SEATS_BY_ROOM_ID = """
SELECT * FROM seats WHERE room_id = ?;
"""


SELECT_COUNT_SEATS_BY_ROOM_ID = """
SELECT COUNT(*) FROM seats WHERE room_id = ?;
"""

SELECT_SEATS_BY_ROOM_NAME_SEAT_CODE = """
SELECT seats.*
FROM seats
JOIN rooms ON seats.room_id = rooms.room_id
WHERE rooms.name = ? AND seats.seat_code = ?;
"""

SELECT_SEATS_BY_ROOM_ID_SEAT_CODE = """
SELECT * FROM seats WHERE room_id = ? AND seat_code = ?;
"""

SELECT_SEATS_BY_ROOM_NAME = """
SELECT seats.*
FROM seats
JOIN rooms ON seats.room_id = rooms.room_id
WHERE rooms.name = ?;
"""

DELETE_SEATS_BY_ROOM_NAME = """
DELETE FROM seats
WHERE room_id = (SELECT room_id FROM rooms WHERE name = ?);
"""

UPDATE_SEAT_STATE = """
UPDATE seats 
SET state = ?
WHERE seat_id = ?;
"""

DELETE_SEAT_BY_ID = """
DELETE FROM seats WHERE seat_id = ?;
"""

DELETE_ALL_SEATS = """
DELETE FROM seats;
"""

TRIGGER_CHECK_SEAT_CAPACITY = """
CREATE TRIGGER IF NOT EXISTS validate_seat_coordinates
BEFORE INSERT ON seats
FOR EACH ROW
BEGIN
    SELECT RAISE(ABORT, 'Row or Column exceeds room dimensions')
    WHERE NEW.row > (SELECT rows FROM rooms WHERE room_id = NEW.room_id)
       OR NEW.col > (SELECT columns FROM rooms WHERE room_id = NEW.room_id);
END;
"""
