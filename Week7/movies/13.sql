SELECT name FROM movies, stars, people
WHERE people.id = stars.person_id
AND stars.movie_id = movies.id
AND NOT name = "Kevin Bacon"
AND title IN
(SELECT title FROM movies, stars, people
WHERE people.id = stars.person_id
AND stars.movie_id = movies.id
AND name = "Kevin Bacon"
AND birth = 1958);