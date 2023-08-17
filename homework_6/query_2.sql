SELECT i.name , s.name , ROUND(AVG(g.grade), 2) as avg_grade 
FROM grades g 
JOIN students s ON s.id = g.id_students 
JOIN items i ON i.id = g.id_items 
WHERE i.id = 5
GROUP BY s.name 
ORDER  BY avg_grade DESC 
LIMIT 1;