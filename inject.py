import unittest, sys
from decimal import Decimal, ROUND_HALF_EVEN
from srms import grading as g
which = sys.argv[1]
if which == "boundary":
    g.subject_passed = lambda marks, mx: Decimal(marks)*100 > g.PASS_PERCENT*Decimal(mx)
else:
    g.percentage = lambda t, m: (Decimal(t)*100/Decimal(m)).quantize(Decimal("0.01"), ROUND_HALF_EVEN)
import tests.test_srms as t
res = unittest.TextTestRunner(stream=open("/dev/null","w")).run(unittest.defaultTestLoader.loadTestsFromModule(t))
print(which, "-> failed:", sorted(str(f[0]).split("_")[1] for f in res.failures+res.errors), "of", res.testsRun)
