SELECT g.name AS group_name, s.name AS student_name
FROM [groups] g 
JOIN students s on g.id = s.id_group 
WHERE g.name = 'TA-1304'
GROUP BY s.name ;