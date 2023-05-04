SELECT name
FROM people
WHERE id IN (
    SELECT DISTINCT(p1.id)
    FROM people AS p1
    JOIN stars AS s1 ON p1.id = s1.person_id AND s1.movie_id IN (
        SELECT s2.movie_id FROM stars AS s2 WHERE s2.person_id = (
            SELECT p2.id FROM people AS p2 WHERE name = "Kevin Bacon" AND birth = 1958
        )
    )
) AND NOT (name = "Kevin Bacon" AND birth = 1958);