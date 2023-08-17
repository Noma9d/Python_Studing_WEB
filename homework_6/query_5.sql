SELECT t.name , i.name 
FROM items i 
JOIN teachers t ON i.id_teacher = t.id 
WHERE t.name = 'Angela Hall';