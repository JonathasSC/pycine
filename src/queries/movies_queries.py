CREATE_MOVIES_TABLE = """
CREATE TABLE IF NOT EXISTS movies (
    movie_id TEXT PRIMARY KEY,
    name TEXT,
    genre TEXT,
    duration TEXT,
    synopsis TEXT
);
"""

INSERT_MOVIE = """
INSERT INTO movies (movie_id, name,  genre, duration, synopsis) 
VALUES (?, ?, ?, ?, ?);
"""

SELECT_ALL_MOVIES = """
SELECT * FROM movies;
"""

SELECT_MOVIE_BY_NAME = """
SELECT *
FROM movies 
WHERE name = ?;
"""


SELECT_MOVIE_BY_ID = """
SELECT *
FROM movies 
WHERE movie_id = ?;
"""

UPDATE_MOVIE = """
UPDATE movies 
SET name = ?, genre = ?, duration = ?, synopsis = ? 
WHERE movie_id = ?;
"""

DELETE_MOVIE = """
DELETE FROM movies 
WHERE movie_id = ?;
"""

DELETE_ALL_MOVIES = """
DELETE FROM movies;
"""
