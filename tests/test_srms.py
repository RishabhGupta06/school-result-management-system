import unittest, sqlite3
from decimal import Decimal as D
from srms import grading as g
from srms.service import ResultService

class UnitTests(unittest.TestCase):                       # 9 unit tests
    def test_TC01_grade_boundary_90_is_A_plus(self):   self.assertEqual(g.grade_for(D("90")), "A+")
    def test_TC02_grade_just_below_90_is_A(self):      self.assertEqual(g.grade_for(D("89.99")), "A")
    def test_TC03_pass_at_exactly_33(self):            self.assertTrue(g.subject_passed(33, 100))
    def test_TC04_fail_at_32(self):                    self.assertFalse(g.subject_passed(32, 100))
    def test_TC05_percentage(self):                    self.assertEqual(g.percentage(425, 500), D("85.00"))
    def test_TC06_rounding_half_up(self):              self.assertEqual(g.percentage(1, 800), D("0.13"))
    def test_TC07_negative_marks_rejected(self):
        with self.assertRaises(ValueError): g.validate_marks(-1, 100)
    def test_TC08_marks_above_max_rejected(self):
        with self.assertRaises(ValueError): g.validate_marks(101, 100)
    def test_TC09_tied_ranks(self):
        self.assertEqual(g.assign_ranks({1: 450, 2: 430, 3: 430, 4: 400}), {1: 1, 2: 2, 3: 2, 4: 4})

class IntegrationTests(unittest.TestCase):               # 6 integration tests
    def setUp(self):
        self.s = ResultService()
        self.c = self.s.add_class("X-A"); self.e = self.s.add_exam("Annual", 2026)
        self.sub = [self.s.add_subject(n) for n in ("English", "Maths", "Science")]
        self.a = self.s.add_student(self.c, "01", "Asha"); self.b = self.s.add_student(self.c, "02", "Bilal")
        for sid, ms in ((self.a, (80, 90, 70)), (self.b, (60, 32, 75))):
            for sub, m in zip(self.sub, ms): self.s.enter_marks(sid, sub, self.e, m)
    def test_TC10_pass_result_and_total(self):
        r = self.s.result(self.a, self.e)
        self.assertEqual((r["total"], r["percent"], r["grade"], r["result"]), (240, D("80.00"), "A", "PASS"))
    def test_TC11_one_failed_subject_fails_and_is_unranked(self):
        self.assertEqual(self.s.result(self.b, self.e)["result"], "FAIL")
        self.assertNotIn(self.b, self.s.class_ranks(self.c, self.e))
    def test_TC12_database_rejects_marks_above_max(self):
        with self.assertRaises(sqlite3.DatabaseError):
            self.s.db.execute("UPDATE marks SET marks=150 WHERE student_id=?", (self.a,))
    def test_TC13_duplicate_marks_entry_rejected(self):
        with self.assertRaises(sqlite3.IntegrityError): self.s.enter_marks(self.a, self.sub[0], self.e, 50)
    def test_TC14_marks_correction_updates_result(self):
        self.s.update_marks(self.b, self.sub[1], self.e, 33)
        self.assertEqual(self.s.result(self.b, self.e)["result"], "PASS")
        self.assertEqual(self.s.class_ranks(self.c, self.e)[self.b], 2)
    def test_TC15_report_card_and_class_summary(self):
        self.assertIn("Total 240/300", self.s.report_card(self.a, self.e))
        self.assertEqual(self.s.class_summary(self.c, self.e)["pass_percent"], D("50.00"))

if __name__ == "__main__":
    unittest.main(verbosity=2)
