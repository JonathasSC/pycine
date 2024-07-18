CREATE_ADMINS_TABLE = """
CREATE TABLE IF NOT EXISTS admins (
    admin_id TEXT PRIMARY KEY,
    person_id TEXT,

    FOREIGN KEY (person_id) REFERENCES persons(person_id)
);
"""

INSERT_ADMIN = """
INSERT INTO admins (admin_id, person_id) VALUES (?, ?)
"""

SELECT_ADMIN_BY_ID = """
SELECT * FROM admins WHERE admin_id = ?;
"""

SELECT_ALL_ADMINS = """
SELECT * FROM admins;
"""

SELECT_ADMIN_BY_PERSON_ID = """
SELECT * FROM admins WHERE person_id = ?;
"""

DELETE_ADMIN = """
DELETE FROM admins WHERE admin_id = ?;
"""

DELETE_ALL_ADMINS = """
DELETE FROM admins;
"""

SELECT_COUNT_ADMINS = """
SELECT COUNT(*) FROM admins;
"""


SELECT_ADMIN_IN_PERSON = """
SELECT 
    p.person_id,
    a.admin_id,
    p.name,
    p.email,
    p.password
FROM
    persons p
JOIN
    admins a 
ON 
    p.person_id = a.person_id;
"""


UPDATE_PERSON_ADMIN_BY_ADMIN_ID = """
UPDATE 
    persons
SET 
    name = ?,
    email = ?,
    password = ?
WHERE 
    person_id = (SELECT person_id FROM admins WHERE admin_id = ?);
"""
