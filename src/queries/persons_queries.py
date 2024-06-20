CREATE_PERSONS_TABLE = """
CREATE TABLE IF NOT EXISTS persons (
    person_id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL
);
"""

UPDATE_PERSON = """
UPDATE persons
SET name = ?, email = ?, password = ?
WHERE person_id = ?;
"""

INSERT_PERSON = """
INSERT INTO persons (person_id, name, email, password) VALUES (?, ?, ?, ?)
"""

SELECT_PERSON_BY_ID = """
SELECT * FROM persons WHERE person_id = ?;
"""

SELECT_PERSON_BY_EMAIL = """
SELECT * FROM persons WHERE email = ?
"""

DELETE_PERSON = """
DELETE FROM persons WHERE person_id = ?;
"""


SELECT_BY_CREDENTIALS = """
SELECT * FROM persons WHERE email = ? AND password = ?;
"""

SELECT_IS_ADMIN = """
SELECT * FROM admins WHERE person_id = ?;
"""

SELECT_IS_CLIENT = """
SELECT * FROM clients WHERE person_id = ?;
"""
