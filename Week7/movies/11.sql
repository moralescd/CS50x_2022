SELECT title FROM movies, ratings, people, stars
WHERE people.id = stars.person_id
AND movies.id = ratings.movie_id
AND stars.movie_id = movies.id
AND name = "Chadwick Boseman"
ORDER BY rating DESC
LIMIT 5;