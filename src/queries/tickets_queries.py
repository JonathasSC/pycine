CREATE_TICKETS_TABLE = """
CREATE TABLE IF NOT EXISTS tickets (
    ticket_id TEXT PRIMARY KEY,
    
    seat_id TEXT,
    person_id TEXT,
    session_id TEXT,

    FOREIGN KEY (seat_id) REFERENCES seats(seat_id),
    FOREIGN KEY (person_id) REFERENCES persons(person_id),
    FOREIGN KEY (session_id) REFERENCES sessions(session_id)
);
"""

INSERT_TICKET = """
INSERT INTO tickets (ticket_id, seat_id, person_id, session_id)
VALUES (?, ?, ?, ?)
"""

SELECT_TICKETS_BY_PERSON_ID = """
SELECT * FROM tickets WHERE person_id = ?
"""

SELECT_TICKETS_BY_ID = """
SELECT * FROM tickets WHERE ticket_id = ?
"""

DELETE_TICKET_BY_ID = """
DELETE FROM tickets
WHERE ticket_id = ?;
"""
