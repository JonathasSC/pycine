CREATE_CLIENTS_TABLE = """
CREATE TABLE IF NOT EXISTS clients (
    client_id TEXT PRIMARY KEY,
    person_id TEXT,
    
    FOREIGN KEY (person_id) REFERENCES persons(person_id)
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
SELECT * FROM clients WHERE client_id = ?;
"""

SELECT_CLIENT_BY_EMAIL = """
SELECT * FROM clients WHERE email = ?;
"""

DELETE_CLIENT_BY_ID = """
DELETE FROM clients WHERE client_id = ?;
"""

DELETE_CLIENT_BY_PERSON_ID = """
DELETE FROM clients WHERE person_id = ?;
"""

SELECT_ALL_CLIENTS = """
SELECT
    c.client_id,
    p.person_id,
    p.name,
    p.email, 
    p.password
FROM 
    clients c
JOIN 
    persons p ON p.person_id = c.person_id
"""

UPDATE_PERSON_CLIENT_BY_CLIENT_ID = """
UPDATE 
    persons
SET 
    name = ?,
    email = ?,
    password = ?
WHERE 
    person_id = (SELECT person_id FROM admins WHERE admin_id = ?);
"""
