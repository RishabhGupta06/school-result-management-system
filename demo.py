from srms.service import ResultService
s = ResultService()
c = s.add_class("X-A"); e = s.add_exam("Annual 2026", 2026)
subs = {n: s.add_subject(n) for n in ["English", "Hindi", "Maths", "Science", "Social Sci"]}
data = {"Aarav Sharma": [88, 76, 94, 91, 85], "Diya Verma": [72, 81, 69, 77, 80],
        "Kabir Singh": [95, 90, 98, 96, 92], "Meera Joshi": [45, 52, 30, 48, 55],
        "Rohan Gupta": [66, 71, 58, 62, 64], "Sana Khan": [88, 76, 94, 91, 85]}
ids = {}
for i, (n, ms) in enumerate(data.items(), start=1):
    ids[n] = s.add_student(c, f"{i:02d}", n)
    for sub, m in zip(subs.values(), ms):
        s.enter_marks(ids[n], sub, e, m)
print(s.report_card(ids["Aarav Sharma"], e)); print()
print(s.report_card(ids["Meera Joshi"], e)); print()
print("Class summary:", s.class_summary(c, e))
print("Ranks:", {n: s.class_ranks(c, e).get(i, "-") for n, i in ids.items()})
