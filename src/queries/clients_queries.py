CREATE_CLIENTS_TABLE = """
CREATE TABLE IF NOT EXISTS clients (
    client_id TEXT PRIMARY KEY,
    person_id TEXT,
    FOREIGN KEY (person_id) REFERENCES persons(id)
);
"""

UPDATE_CLIENT = """
UPDATE clients
SET name = ?, email = ?, password = ?
WHERE id = ?;
"""

INSERT_CLIENT = """
INSERT INTO clients (client_id, person_id) VALUES (?, ?);
"""

SELECT_CLIENT_BY_ID = """
SELECT * FROM clients WHERE id = ?;
"""

SELECT_CLIENT_BY_EMAIL = """
SELECT * FROM clients WHERE email = ?;
"""

DELETE_CLIENT = """
DELETE FROM clients WHERE id = ?;
"""
