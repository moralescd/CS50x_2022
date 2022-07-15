SELECT title FROM movies, stars, people
WHERE people.id = stars.person_id
AND stars.movie_id = movies.id
AND name = "Johnny Depp"
INTERSECT
SELECT title FROM movies, stars, people
WHERE people.id = stars.person_id
AND stars.movie_id = movies.id
AND name = "Helena Bonham Carter";
