from decimal import Decimal, ROUND_HALF_UP

PASS_PERCENT = Decimal("33")          # configurable pass mark (percent of max marks)
GRADE_SCALE = [(Decimal("90"), "A+"), (Decimal("80"), "A"), (Decimal("70"), "B"),
               (Decimal("60"), "C"), (Decimal("50"), "D"), (Decimal("33"), "E")]

def validate_marks(marks, max_marks):
    if not isinstance(marks, int) or marks < 0 or marks > max_marks:
        raise ValueError(f"marks must be an integer between 0 and {max_marks}")
    return marks

def percentage(total, max_total):
    if max_total <= 0:
        raise ValueError("max_total must be positive")
    return (Decimal(total) * 100 / Decimal(max_total)).quantize(Decimal("0.01"), ROUND_HALF_UP)

def grade_for(percent):
    for limit, grade in GRADE_SCALE:
        if percent >= limit:
            return grade
    return "F"

def subject_passed(marks, max_marks):
    return Decimal(marks) * 100 >= PASS_PERCENT * Decimal(max_marks)

def assign_ranks(totals):
    """totals: {student_id: total}. Competition ranking (1,2,2,4)."""
    ordered = sorted(totals.items(), key=lambda kv: -kv[1])
    ranks, prev, rank = {}, None, 0
    for i, (sid, tot) in enumerate(ordered, start=1):
        if tot != prev:
            rank = i
            prev = tot
        ranks[sid] = rank
    return ranks
