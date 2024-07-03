CREATE_SEATS_TABLE = """
CREATE TABLE IF NOT EXISTS seats (
    seat_id TEXT PRIMARY KEY,
    room_id TEXT,
    seat_code TEXT,
    row INTEGER,
    col INTEGER,
    state TEXT CHECK (state IN ('reserved', 'sold', 'available')),
    FOREIGN KEY (room_id) REFERENCES rooms(room_id)
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
SELECT * FROM seats WHERE id = ?;
"""

SELECT_SEATS_BY_ROOM_ID = """
SELECT * FROM seats WHERE room_id = ?;
"""

UPDATE_SEAT = """
UPDATE seats 
SET room_id = ?, row = ?, number = ?, is_available = ? 
WHERE id = ?;
"""

DELETE_SEAT = """
DELETE FROM seats WHERE id = ?;
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
