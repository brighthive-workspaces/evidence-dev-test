SELECT 
  major,
  COUNT(student_id) AS student_count
FROM database_891377033216.students
GROUP BY major;