SELECT t.name as teacher_name , i.name as items_name , ROUND(AVG(g.grade), 2) as avg_grade 
FROM teachers t 
JOIN items i ON i.id_teacher = t.id 
JOIN grades g ON g.id_items = i.id 
WHERE t.name = 'Angela Hall'
GROUP BY t.name , i.name ;