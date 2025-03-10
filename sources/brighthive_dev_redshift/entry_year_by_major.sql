SELECT 
  major, 
  entry_year, 
  COUNT(student_id) AS student_count
FROM database_891377033216.students
GROUP BY major, entry_year
ORDER BY major, entry_year;