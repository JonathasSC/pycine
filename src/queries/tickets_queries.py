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
"""
