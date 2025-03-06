SELECT
    final_grade,
    COUNT(*) AS student_count
FROM
    database_891377033216.academic_performance
GROUP BY
    final_grade
ORDER BY
    student_count DESC;
