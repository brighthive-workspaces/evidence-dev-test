SELECT 
    course_id, 
    CAST(AVG(
        CASE 
            WHEN final_grade = 'A' THEN 4.0
            WHEN final_grade = 'B' THEN 3.0
            WHEN final_grade = 'C' THEN 2.0
            WHEN final_grade = 'D' THEN 1.0
            ELSE 0.0
        END
    ) AS FLOAT) AS average_final_grade
FROM 
    database_891377033216.academic_performance
GROUP BY 
    course_id
ORDER BY 
    average_final_grade DESC;