import sqlite3, pathlib
from . import grading as g

SCHEMA = pathlib.Path(__file__).with_name("schema.sql").read_text()

class ResultService:
    def __init__(self, path=":memory:"):
        self.db = sqlite3.connect(path)
        self.db.executescript(SCHEMA)

    # ---- master data ----
    def add_class(self, name):
        return self.db.execute("INSERT INTO class(name) VALUES(?)", (name,)).lastrowid
    def add_student(self, class_id, roll_no, name):
        return self.db.execute("INSERT INTO student(class_id,roll_no,name) VALUES(?,?,?)",
                               (class_id, roll_no, name)).lastrowid
    def add_subject(self, name, max_marks=100):
        return self.db.execute("INSERT INTO subject(name,max_marks) VALUES(?,?)", (name, max_marks)).lastrowid
    def add_exam(self, name, year):
        return self.db.execute("INSERT INTO exam(name,year) VALUES(?,?)", (name, year)).lastrowid

    # ---- marks ----
    def enter_marks(self, student_id, subject_id, exam_id, marks):
        mx = self.db.execute("SELECT max_marks FROM subject WHERE subject_id=?", (subject_id,)).fetchone()[0]
        g.validate_marks(marks, mx)
        self.db.execute("INSERT INTO marks VALUES(?,?,?,?)", (student_id, subject_id, exam_id, marks))
    def update_marks(self, student_id, subject_id, exam_id, marks):
        mx = self.db.execute("SELECT max_marks FROM subject WHERE subject_id=?", (subject_id,)).fetchone()[0]
        g.validate_marks(marks, mx)
        self.db.execute("UPDATE marks SET marks=? WHERE student_id=? AND subject_id=? AND exam_id=?",
                        (marks, student_id, subject_id, exam_id))

    # ---- results ----
    def result(self, student_id, exam_id):
        rows = self.db.execute("""SELECT s.name, m.marks, s.max_marks FROM marks m
              JOIN subject s ON s.subject_id=m.subject_id
              WHERE m.student_id=? AND m.exam_id=? ORDER BY s.name""", (student_id, exam_id)).fetchall()
        total = sum(r[1] for r in rows); max_total = sum(r[2] for r in rows)
        pct = g.percentage(total, max_total)
        subjects = [(n, m, mx, g.grade_for(g.percentage(m, mx)), g.subject_passed(m, mx)) for n, m, mx in rows]
        passed = all(s[4] for s in subjects)
        return {"subjects": subjects, "total": total, "max_total": max_total, "percent": pct,
                "grade": g.grade_for(pct), "result": "PASS" if passed else "FAIL"}

    def class_ranks(self, class_id, exam_id):
        ids = [r[0] for r in self.db.execute("SELECT student_id FROM student WHERE class_id=?", (class_id,))]
        res = {i: self.result(i, exam_id) for i in ids}
        passed = {i: r["total"] for i, r in res.items() if r["result"] == "PASS"}
        return g.assign_ranks(passed)

    def class_summary(self, class_id, exam_id):
        ids = [r[0] for r in self.db.execute("SELECT student_id FROM student WHERE class_id=?", (class_id,))]
        res = [self.result(i, exam_id) for i in ids]
        n = len(res); p = sum(1 for r in res if r["result"] == "PASS")
        avg = (sum(r["percent"] for r in res) / n).quantize(g.Decimal("0.01"), g.ROUND_HALF_UP)
        return {"students": n, "passed": p, "pass_percent": g.percentage(p, n), "average_percent": avg}

    def report_card(self, student_id, exam_id):
        name, roll, cls = self.db.execute("""SELECT s.name, s.roll_no, c.name FROM student s
              JOIN class c ON c.class_id=s.class_id WHERE s.student_id=?""", (student_id,)).fetchone()
        r = self.result(student_id, exam_id)
        rank = self.class_ranks(self.db.execute("SELECT class_id FROM student WHERE student_id=?", (student_id,)).fetchone()[0], exam_id).get(student_id, "-")
        L = [f"REPORT CARD   {name} (Roll {roll}, Class {cls})", "-" * 52,
             f"{'Subject':<14}{'Marks':>8}{'Max':>6}{'Grade':>8}{'Status':>8}"]
        for n, m, mx, gr, ok in r["subjects"]:
            L.append(f"{n:<14}{m:>8}{mx:>6}{gr:>8}{('Pass' if ok else 'Fail'):>8}")
        L += ["-" * 52, f"Total {r['total']}/{r['max_total']}   Percentage {r['percent']}%   Grade {r['grade']}",
              f"Result: {r['result']}   Class rank: {rank}"]
        return "\n".join(L)
