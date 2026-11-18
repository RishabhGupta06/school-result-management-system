# Software Requirements Specification (IEEE 830 style) - School Result Management System (SRMS)

Author: Rishabh Gupta (01314803124)

## 1. Introduction
Purpose: define the requirements of SRMS, a system that records marks, computes results and publishes report cards for a school.
Users: Admin, Teacher, Student / Parent.

## 2. Functional requirements (19)
| ID | Requirement | In prototype |
|----|-------------|--------------|
| FR1 | Users log in with a role (Admin / Teacher / Student) | design only |
| FR2 | Admin manages classes | yes |
| FR3 | Admin adds students; roll number is unique within a class | yes (add) |
| FR4 | Admin manages subjects and their maximum marks | yes |
| FR5 | Admin manages teachers and assigns them to class-subject pairs | schema only |
| FR6 | Admin creates exams | yes |
| FR7 | Teacher enters marks for a student, subject and exam | yes |
| FR8 | System accepts only integer marks from 0 to the subject maximum | yes (TC07, TC08, TC12) |
| FR9 | System rejects a second entry for the same student, subject and exam | yes (TC13) |
| FR10 | Marks can be corrected; result and ranks update | yes (TC14) |
| FR11 | System computes the total marks | yes (TC10) |
| FR12 | System computes percentage to 2 decimals, rounded half-up | yes (TC05, TC06) |
| FR13 | System assigns a grade from the scale A+ (>=90), A, B, C, D, E (>=33), F | yes (TC01, TC02) |
| FR14 | A subject is passed at 33% or more; overall PASS only if all subjects pass | yes (TC03, TC04, TC11) |
| FR15 | PASS students are ranked by total; ties share a rank | yes (TC09) |
| FR16 | System generates a report card per student | yes (TC15) |
| FR17 | System produces a class summary (pass percentage, average) | yes (TC15) |
| FR18 | Admin publishes results; students see only published results | design only |
| FR19 | Report card can be printed / downloaded as PDF | design only |

## 3. Non-functional requirements (8)
| ID | Requirement |
|----|-------------|
| NFR1 | Accuracy: all percentage arithmetic uses exact decimal numbers |
| NFR2 | Performance: a class result (up to 60 students) is produced in under 2 seconds |
| NFR3 | Security: role-based access; passwords stored hashed |
| NFR4 | Usability: a teacher can enter a subject's marks for a class in one screen |
| NFR5 | Data integrity: invalid and duplicate marks are rejected by database constraints |
| NFR6 | Portability: runs on SQLite (prototype) and MySQL (deployment) |
| NFR7 | Maintainability: modular code with automated unit and integration tests |
| NFR8 | Availability: daily database backup |
