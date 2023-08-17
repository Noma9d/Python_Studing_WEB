SELECT i.name , grou.name , ROUND(AVG(g.grade), 2) as avg_grade 
FROM grades g 
JOIN students s ON s.id = g.id_students 
JOIN items i ON i.id = g.id_items 
JOIN [groups] grou ON grou.id = s.id_group 
WHERE i.id = 5
GROUP BY grou.name, i.name 
ORDER  BY avg_grade DESC;