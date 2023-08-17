SELECT s.name , ROUND(AVG(g.grade), 2) as avg_grade 
FROM grades g 
LEFT JOIN students s ON s.id = g.id_students 
GROUP BY s.name 
ORDER  BY avg_grade DESC 
LIMIT 5;