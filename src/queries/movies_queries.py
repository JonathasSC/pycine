CREATE_MOVIES_TABLE = """
CREATE TABLE IF NOT EXISTS movies (
    movie_id TEXT PRIMARY KEY,
    name TEXT UNIQUE NOT NULL,
    genre TEXT NOT NULL,
    duration TEXT NOT NULL,
    synopsis TEXT NOT NULL
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

DELETE_MOVIE_BY_NAME = """
DELETE FROM movies 
WHERE name = ?;
"""

DELETE_MOVIE_BY_ID = """
DELETE FROM movies 
WHERE movie_id = ?;
"""

DELETE_ALL_MOVIES = """
DELETE FROM movies;
"""
