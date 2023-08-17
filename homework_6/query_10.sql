SELECT s.name AS student_name, i.name AS items_name, t.name AS teacher_name
FROM items i
JOIN students s  ON s.id = g.id_students 
JOIN grades g ON g.id_items = i.id 
JOIN teachers t ON t.id = i.id_teacher 
WHERE s.name = 'Gloria Fleming' AND t.name = 'Angela Hall'
ORDER BY i.name ;