SELECT
    final_grade,
    COUNT(*) AS student_count
FROM
    brighthive_dev_redshift.academic_performance_1738358525184
GROUP BY
    final_grade
ORDER BY
    student_count DESC;
