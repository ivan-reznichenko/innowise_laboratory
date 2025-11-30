/*
    Student Grades Manager - SQL Queries
    Target Database: school.db
*/

-- =============================================================
-- SECTION 1: CREATE TABLES
-- =============================================================

-- Enable Foreign Key support in SQLite
PRAGMA foreign_keys = ON;

-- 1. Create 'students' table
-- Represents the personal information of the students.
CREATE TABLE IF NOT EXISTS students (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    full_name TEXT NOT NULL,
    birth_year INTEGER NOT NULL
);

-- 2. Create 'grades' table
-- Represents the academic performance linked to students.
CREATE TABLE IF NOT EXISTS grades (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id INTEGER NOT NULL,
    subject TEXT NOT NULL,
    grade INTEGER NOT NULL CHECK(grade BETWEEN 0 AND 100),
    FOREIGN KEY (student_id) REFERENCES students(id) ON DELETE CASCADE
);

-- =============================================================
-- SECTION 2: OPTIMIZATION (INDEXES)
-- =============================================================

-- Index for faster joins and lookups by student_id in the grades table
CREATE INDEX IF NOT EXISTS idx_grades_student_id ON grades(student_id);

-- Index for faster filtering of students by their birth year
CREATE INDEX IF NOT EXISTS idx_students_birth_year ON students(birth_year);

-- Index for faster aggregation by subject
CREATE INDEX IF NOT EXISTS idx_grades_subject ON grades(subject);

-- =============================================================
-- SECTION 3: INSERT SAMPLE DATA
-- =============================================================

-- Inserting Students
INSERT INTO students (full_name, birth_year) VALUES 
('Alice Johnson', 2005),
('Brian Smith', 2004),
('Carla Reyes', 2006),
('Daniel Kim', 2005),
('Eva Thompson', 2003),
('Felix Nguyen', 2007),
('Grace Patel', 2005),
('Henry Lopez', 2004),
('Isabella Martinez', 2006);

-- Inserting Grades
-- Note: Assuming student IDs match the order of insertion (1 to 9)
INSERT INTO grades (student_id, subject, grade) VALUES 
(1, 'Math', 88), (1, 'English', 92), (1, 'Science', 85),
(2, 'Math', 75), (2, 'History', 83), (2, 'English', 79),
(3, 'Science', 95), (3, 'Math', 91), (3, 'Art', 89),
(4, 'Math', 84), (4, 'Science', 88), (4, 'Physical Education', 93),
(5, 'English', 90), (5, 'History', 85), (5, 'Math', 88),
(6, 'Science', 72), (6, 'Math', 78), (6, 'English', 81),
(7, 'Art', 94), (7, 'Science', 87), (7, 'Math', 90),
(8, 'History', 77), (8, 'Math', 83), (8, 'Science', 80),
(9, 'English', 96), (9, 'Math', 89), (9, 'Art', 92);

-- =============================================================
-- SECTION 4: ANALYTICAL QUERIES
-- =============================================================

-- Query 1: Find all grades for a specific student (Alice Johnson)
-- We join tables to filter by name rather than hardcoding the ID.
SELECT 
    s.full_name, 
    g.subject, 
    g.grade
FROM grades g
JOIN students s ON g.student_id = s.id
WHERE s.full_name = 'Alice Johnson';

-- Query 2: Calculate the average grade per student
-- Groups results by student to show their overall performance.
SELECT 
    s.full_name, 
    ROUND(AVG(g.grade), 2) as average_grade
FROM students s
JOIN grades g ON s.id = g.student_id
GROUP BY s.id, s.full_name;

-- Query 3: List all students born after 2004
-- Simple filtering based on the birth_year column.
SELECT 
    full_name, 
    birth_year
FROM students
WHERE birth_year > 2004;

-- Query 4: List all subjects and their average grades
-- Helps analyze which subjects are "easier" or "harder" on average.
SELECT 
    subject, 
    ROUND(AVG(grade), 2) as subject_avg_grade
FROM grades
GROUP BY subject
ORDER BY subject_avg_grade DESC;

-- Query 5: Find the top 3 students with the highest average grades
-- Sorts the average calculation descending and limits to 3.
SELECT 
    s.full_name, 
    ROUND(AVG(g.grade), 2) as average_grade
FROM students s
JOIN grades g ON s.id = g.student_id
GROUP BY s.id, s.full_name
ORDER BY average_grade DESC
LIMIT 3;

-- Query 6: Show all students who have scored below 80 in any subject
-- Uses DISTINCT to avoid listing the same student multiple times if they have multiple low grades.
SELECT DISTINCT 
    s.full_name
FROM students s
JOIN grades g ON s.id = g.student_id
WHERE g.grade < 80;