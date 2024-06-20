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

SELECT_ADMIN_BY_PERSON_ID = """
SELECT * FROM admins WHERE person_id = ?;
"""

DELETE_ADMIN = """
DELETE FROM admins WHERE admin_id = ?;
"""

SELECT_COUNT_ADMINS = """
SELECT COUNT(*) FROM admins;
"""
