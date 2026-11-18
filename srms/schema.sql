PRAGMA foreign_keys = ON;
CREATE TABLE class      (class_id INTEGER PRIMARY KEY, name TEXT NOT NULL UNIQUE);
CREATE TABLE student    (student_id INTEGER PRIMARY KEY, roll_no TEXT NOT NULL,
                         name TEXT NOT NULL, class_id INTEGER NOT NULL REFERENCES class(class_id),
                         UNIQUE(class_id, roll_no));
CREATE TABLE teacher    (teacher_id INTEGER PRIMARY KEY, name TEXT NOT NULL, username TEXT NOT NULL UNIQUE,
                         role TEXT NOT NULL CHECK(role IN ('ADMIN','TEACHER')));
CREATE TABLE subject    (subject_id INTEGER PRIMARY KEY, name TEXT NOT NULL UNIQUE,
                         max_marks INTEGER NOT NULL CHECK(max_marks > 0));
CREATE TABLE class_subject (class_id INTEGER NOT NULL REFERENCES class(class_id),
                         subject_id INTEGER NOT NULL REFERENCES subject(subject_id),
                         teacher_id INTEGER REFERENCES teacher(teacher_id),
                         PRIMARY KEY(class_id, subject_id));
CREATE TABLE exam       (exam_id INTEGER PRIMARY KEY, name TEXT NOT NULL UNIQUE, year INTEGER NOT NULL);
CREATE TABLE marks      (student_id INTEGER NOT NULL REFERENCES student(student_id),
                         subject_id INTEGER NOT NULL REFERENCES subject(subject_id),
                         exam_id INTEGER NOT NULL REFERENCES exam(exam_id),
                         marks INTEGER NOT NULL CHECK(marks >= 0),
                         UNIQUE(student_id, subject_id, exam_id));
CREATE TRIGGER marks_max_ins BEFORE INSERT ON marks
WHEN NEW.marks > (SELECT max_marks FROM subject WHERE subject_id = NEW.subject_id)
BEGIN SELECT RAISE(ABORT, 'marks exceed subject maximum'); END;
CREATE TRIGGER marks_max_upd BEFORE UPDATE ON marks
WHEN NEW.marks > (SELECT max_marks FROM subject WHERE subject_id = NEW.subject_id)
BEGIN SELECT RAISE(ABORT, 'marks exceed subject maximum'); END;
