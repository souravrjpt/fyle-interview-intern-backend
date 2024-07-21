-- Write query to get number of graded assignments for each student:
SELECT * FROM assignments WHERE state = 'GRADED' GROUP BY student_id 