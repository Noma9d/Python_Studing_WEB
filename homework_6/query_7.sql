SELECT g.name AS groups_name, s.name AS student_name , g2.grade AS grades_name, i.name AS items_name
FROM [groups] g 
JOIN students s ON g.id = s.id_group 
JOIN grades g2 ON g2.id_students = s.id 
JOIN items i ON i.id = g2.id_items 
WHERE g.name = 'TA-1304'
AND i.name = 'math';