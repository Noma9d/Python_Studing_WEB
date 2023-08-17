SELECT s.name AS student_name, i.name AS items_name
FROM students s     
JOIN items i ON i.id = g.id_items 
JOIN grades g ON g.id_students = s.id 
WHERE s.name = 'Gloria Fleming'
GROUP BY s.name , i.name ;