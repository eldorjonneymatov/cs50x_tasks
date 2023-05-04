SELECT movies.title
FROM movies
JOIN stars ON movies.id = stars.movie_id AND stars.person_id = (
    SELECT id FROM people WHERE name = "Chadwick Boseman"
)
JOIN ratings ON movies.id = ratings.movie_id
ORDER BY ratings.rating DESC
LIMIT 5;