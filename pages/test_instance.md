```sql attendance_by_course
select
    course_id,
    attendance_rate
from
    brighthive_dev_redshift.academic_performance
where
    final_grade = 'A'
order by
    attendance_rate desc;
```

<BarChart
    data={attendance_by_course}
    x=course_id
    y=attendance_rate
    labels=true
    yFmt="0.0%"
    colorPalette={["#76b7b2"]}
    title="Average Attendance Rate by Course for Students with Grade 'A'"
/>
