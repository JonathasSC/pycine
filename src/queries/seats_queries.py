CREATE_SEATS_TABLE = """
CREATE TABLE IF NOT EXISTS seats (
    seat_id TEXT PRIMARY KEY,
    room_id TEXT,

    line TEXT,
    column TEXT,

    state TEXT CHECK (state in ('reserved', 'sold', 'available')),
    FOREIGN KEY (room_id) REFERENCES rooms(id)
);
"""

INSERT_SEAT = """
INSERT INTO seats (seat_id, room_id, line, column, state)
VALUES (?, ?, ?, ?, ?);
"""


INSERT_SEAT = """
INSERT INTO seats (id, room_id, row, number, is_available) 
VALUES (?, ?, ?, ?, ?);
"""

SELECT_SEAT_BY_ID = """
SELECT * FROM seats WHERE id = ?;
"""

UPDATE_SEAT = """
UPDATE seats 
SET room_id = ?, row = ?, number = ?, is_available = ? 
WHERE id = ?;
"""

DELETE_SEAT = """
DELETE FROM seats WHERE id = ?;
"""

TRIGGER_CHECK_SEAT_CAPACITY = """
CREATE TRIGGER IF NOT EXISTS check_seat_capacity
BEFORE INSERT ON seats
FOR EACH ROW 
BEGIN
    SELECT
        CASE 
            WHEN (
                SELECT COUNT(*) FROM seats WHERE room_id = NEW.room_id
            ) >= (
                SELECT rows * columns FROM room WHERE room_id = NEW.room_id
            )
            THEN 
                RAISE(ABORT, 'A capacidade da sala foi excedida')
        END;
END;
"""
