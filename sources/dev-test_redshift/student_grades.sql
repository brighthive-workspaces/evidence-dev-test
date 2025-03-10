SELECT 
    final_grade, 
    COUNT(DISTINCT student_id) AS student_count 
FROM 
    database_891377033216.academic_performance 
GROUP BY final_grade;