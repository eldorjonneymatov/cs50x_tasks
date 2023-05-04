SELECT movies.title
FROM movies
JOIN stars AS s1 ON movies.id = s1.movie_id AND s1.person_id IN (
    SELECT id FROM people WHERE name = "Johnny Depp"
)
JOIN stars AS s2 ON movies.id = s2.movie_id AND s2.person_id IN (
    SELECT id FROM people WHERE name = "Helena Bonham Carter"
);