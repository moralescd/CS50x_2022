SELECT name from people WHERE id IN
(SELECT person_id FROM stars WHERE movie_id IN
(select id FROM movies WHERE year = 2004))
ORDER BY birth;