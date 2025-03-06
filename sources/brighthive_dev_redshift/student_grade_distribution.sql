SELECT
    final_grade,
    COUNT(*) AS student_count
FROM
    brighthive_dev_redshift.academic_performance
GROUP BY
    final_grade
ORDER BY
    student_count DESC;
