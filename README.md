# School Result Management System (SRMS)

Software Engineering mini project (CIC-357) - Rishabh Gupta, 01314803124, B.Tech IT, MAIT Delhi.

Prototype of the result-processing core: marks validation, percentage, grade, pass/fail, class ranks,
report card and class summary, on an SQLite schema with PK / FK / UNIQUE / CHECK constraints and triggers.

## Run
    python3 demo.py                      # prints sample report cards and class summary
    python3 -m unittest -v tests.test_srms   # 15 tests (9 unit, 6 integration)
    python3 inject.py boundary           # injected fault: pass check >= -> >   (TC03, TC14 fail)
    python3 inject.py rounding           # injected fault: half-up -> half-even (TC06 fails)
    python3 estimate.py                  # function points and PERT / critical path

Requires Python 3.9+ (standard library only). Diagrams: `figs.py`, `figs2.py` (need graphviz + matplotlib).
See `SRS.md` for the requirements.
