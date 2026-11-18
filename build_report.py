import json
from PIL import Image
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_JUSTIFY, TA_CENTER
from reportlab.platypus import (BaseDocTemplate, PageTemplate, Frame, Paragraph, Spacer, Table, TableStyle,
    Image as RLImage, Preformatted, KeepTogether, HRFlowable)
E=json.load(open("est.json"))
NAME="Rishabh Gupta"; ENR="01314803124"
W,H=A4; LM=15*mm; CW=W-2*LM
body=ParagraphStyle("b",fontName="Times-Roman",fontSize=10.5,leading=12.8,alignment=TA_JUSTIFY,spaceAfter=2.5)
bul=ParagraphStyle("bl",parent=body,leftIndent=11,bulletIndent=1,spaceAfter=1.5)
h1=ParagraphStyle("h1",fontName="Times-Bold",fontSize=16,leading=19,alignment=TA_CENTER,spaceAfter=3)
h2=ParagraphStyle("h2",fontName="Times-Bold",fontSize=11.5,leading=13.5,spaceBefore=5,spaceAfter=2)
cap=ParagraphStyle("cap",fontName="Times-Roman",fontSize=7.3,leading=8.6,alignment=TA_JUSTIFY)
code=ParagraphStyle("code",fontName="Courier",fontSize=7.6,leading=9)
def P(t,s=body): return Paragraph(t,s)
def B(t): return Paragraph(t,bul,bulletText="\u2022")
def H2(t): return [P(t,h2),HRFlowable(width="100%",thickness=0.4,color=colors.grey,spaceAfter=3)]

def row(items,maxh=40,gap=3):
    """items: list of (img, caption). equal height, widths by aspect"""
    asp=[Image.open(f"figs/{f}.png").size for f,_ in items]; asp=[w/h for w,h in asp]
    h=min(maxh*mm,(CW-gap*mm*(len(items)-1))/sum(asp)/1.0)
    ws=[a*h for a in asp]
    cells=[RLImage(f"figs/{f}.png",width=w,height=h) for (f,_),w in zip(items,ws)]
    caps=[Paragraph(c,cap) for _,c in items]
    cw=[w+gap*mm+2 for w in ws]
    t=Table([cells,caps],colWidths=cw,hAlign="CENTER")
    t.setStyle(TableStyle([("VALIGN",(0,0),(-1,0),"MIDDLE"),("BOX",(0,0),(-1,0),0.3,colors.lightgrey),
      ("LEFTPADDING",(0,0),(-1,-1),2),("RIGHTPADDING",(0,0),(-1,-1),5),("TOPPADDING",(0,0),(-1,-1),1.5),("BOTTOMPADDING",(0,0),(-1,-1),2)]))
    return KeepTogether([t,Spacer(1,3)])

def footer(c,doc):
    c.saveState(); c.setFont("Times-Roman",8)
    c.setFillColor(colors.grey)
    c.drawCentredString(W/2,9*mm,f"{NAME} | {ENR} | IT, 5th Sem | Software Engineering \u2013 Mini Project | Page {doc.page}")
    c.restoreState()
doc=BaseDocTemplate("/mnt/user-data/outputs/Mini_Project_SE_Rishabh_Gupta.pdf",pagesize=A4,title="Mini Project - School Result Management System",author=NAME)
doc.addPageTemplates([PageTemplate(id="m",frames=[Frame(LM,15*mm,CW,H-27*mm,leftPadding=0,rightPadding=0,topPadding=0,bottomPadding=0)],onPage=footer)])

endw=E["end"]; p95=endw+1.645*E["sd"]
S=[P("MINI PROJECT \u2013 SE",h1),HRFlowable(width="100%",thickness=1.2,color=colors.black,spaceAfter=3),
P("<b>Project Title:</b> School Result Management System (SRMS)"),
]
S+=H2("<b>Student Details</b>")
sd=Table([[P(f"<b>Student Name:</b> {NAME}"),P(f"<b>Enrollment Number:</b> {ENR}")],
          [P("<b>Course / Semester:</b> B.Tech (IT) / 5th Semester"),P("<b>Subject:</b> Software Engineering (CIC-357)")],
          [P("<b>Institute:</b> Maharaja Agrasen Institute of Technology"),P("<b>Faculty:</b> Nidhi Sengar")]],colWidths=[CW*0.55,CW*0.45])
sd.setStyle(TableStyle([("LEFTPADDING",(0,0),(-1,-1),0),("TOPPADDING",(0,0),(-1,-1),0.5),("BOTTOMPADDING",(0,0),(-1,-1),0.5)])); S.append(sd)
S+=H2("<b>Abstract</b>")
S.append(P(f"Many schools still prepare marksheets and result lists by hand or in loose spreadsheets, which leads to addition errors, wrong grades, "
f"delays in declaring results and no easy way to correct a mark or rank students. This project analyses and designs a School Result Management System (SRMS) for "
f"teachers, administrators and students. Following the software engineering life cycle, we wrote the problem statement and an IEEE 830 SRS, then modelled the system with "
f"DFD, ER, UML, component and deployment diagrams. A Python prototype with an SQLite schema was built, and all 15 unit and integration test cases pass. Effort was estimated at "
f"{E['fp']:.2f} function points ({E['pm']:.2f} person-months) and the schedule is about {endw:.1f} weeks on the critical path. The outcome is a complete, traceable design for fast and accurate result processing."))
S+=H2("<b>Problem Statement</b>")
S.append(P("Schools depend on manual or semi-manual result preparation, so marks are added wrongly, grades and pass/fail decisions are inconsistent, class ranks are slow to produce, "
"and a correction after publication is hard to trace. A simple, fast and reliable system is needed that lets a teacher enter marks with validation, computes total, percentage, grade, "
"result and rank by fixed rules, generates a report card for every student and stores all marks so that results can be reviewed or corrected later."))
S+=H2("<b>Objectives</b>")
S+= [B("<b>Objective 1:</b> Document the problem and requirements: problem statement and an IEEE 830 SRS (19 functional and 8 non-functional requirements)."),
B("<b>Objective 2:</b> Model the system through function-oriented (DFD, structure chart), data (ER) and object-oriented (UML) views."),
B("<b>Objective 3:</b> Implement and test the result logic (validation, percentage, grade, pass/fail, rank), estimate effort with Function Points and plan the schedule with Gantt and PERT charts.")]
S+=H2("<b>Methodology / Approach</b>")
S.append(P("The project followed the software development life cycle: requirements, design, implementation and testing, then estimation and scheduling. The diagram produced in each phase is shown below with a short explanation."))
S.append(row([("f01","<b>Fig. 1 System flowchart:</b> login, marks entry with 0-to-maximum validation, save, result and rank computation, report card."),
 ("f02","<b>Fig. 2 Use case:</b> 3 actors and 12 use cases; Generate Report Card and View Result include Calculate Result, Update Marks extends Enter Marks."),
 ("f03","<b>Fig. 3 DFD Level-1:</b> 5 processes (Manage Master Data to Publish / View Results) and 4 data stores, with Admin, Teacher and Student as external entities.")],maxh=50))
S.append(row([("f04","<b>Fig. 4 Structure chart:</b> main module with 5 first-level and 14 lower-level modules."),
 ("f05","<b>Fig. 5 ER diagram:</b> 5 entities and 4 relationships (1:N, M:N, ternary) mapped to 7 database tables."),
 ("f06","<b>Fig. 6 Class diagram:</b> User (Admin, Teacher), SchoolClass, Student, Subject, Exam, MarkEntry, ResultService and Grading.")],maxh=48))
S.append(row([("f07","<b>Fig. 7 Object diagram:</b> snapshot of one student (Aarav Sharma) with 434 / 500 marks, 86.80%, grade A, PASS, rank 2."),
 ("f08","<b>Fig. 8 State-chart:</b> marksheet life cycle: Draft, Submitted, Verified, Published, Under Correction."),
 ("f09","<b>Fig. 9 Activity diagram:</b> workflow in Teacher, System and Admin swimlanes with a decision and fork/join.")],maxh=44))
S.append(row([("f10","<b>Fig. 10 Sequence diagram:</b> time-ordered messages to enter marks (valid / invalid) and view a result."),
 ("f11","<b>Fig. 11 Collaboration diagram:</b> the same interaction as numbered messages between objects."),
 ("f12","<b>Fig. 12 Component diagram:</b> UI, Auth, Student, Marks, Result Engine and Report components over a data-access layer.")],maxh=44))
S.append(row([("f13","<b>Fig. 13 Deployment diagram:</b> teacher, admin and student devices, application server, database server and printer."),
 ("f14",f"<b>Fig. 14 Timeline / Gantt:</b> plan from analysis to deployment with milestones M1 to M4; critical path {endw:.1f} weeks.")],maxh=44))
S.append(row([("f15",f"<b>Fig. 15 PERT chart:</b> activity-on-node network (te in weeks; ES and EF below). Critical path A-B-C-E-F-G-I-J-K = {endw:.1f} weeks; 95% chance of finishing within {p95:.1f} weeks.")],maxh=34))

S+=H2("<b>Implementation &amp; Output</b>")
S+=[B("<b>Python 3 prototype</b> (<font name='Courier'>srms</font> package): <font name='Courier'>grading</font> (percentage, grade, pass mark, ranks), <font name='Courier'>ResultService</font> (marks entry and correction, result, class ranks, class summary, report card) and an in-memory demo."),
B("<b>SQLite schema</b> (portable to MySQL): 7 tables with primary, foreign, UNIQUE and CHECK constraints; a mark above the subject maximum or a duplicate entry is rejected by the database itself."),
B("<b>Rules used:</b> integer marks from 0 to the subject maximum; subject pass at 33% or more; overall PASS only if every subject passes; grade scale A+ (90 and above), A, B, C, D, E (33 and above), F; PASS students are ranked by total, ties share a rank."),
B("<b>Scope:</b> the prototype covers the core result processing (FR2 to FR4 and FR6 to FR17 in the SRS); login, teacher assignment, publishing and the web interface are design-level and listed under Future Scope."),
P("Sample report card produced by the prototype (class X-A, 6 students, Annual 2026):")]
rc='''REPORT CARD   Aarav Sharma (Roll 01, Class X-A)
----------------------------------------------------
Subject          Marks   Max   Grade  Status
English             88   100       A    Pass
Hindi               76   100       B    Pass
Maths               94   100      A+    Pass
Science             91   100      A+    Pass
Social Sci          85   100       A    Pass
----------------------------------------------------
Total 434/500   Percentage 86.80%   Grade A
Result: PASS   Class rank: 2'''
cs='''Class summary (6 students):  passed 5,  pass percentage 83.33%,  average 75.63%
Failed: Meera Joshi (Maths 30 / 100, below the 33% pass mark) -> Result FAIL, unranked
Ranks: Kabir Singh 1, Aarav Sharma 2, Sana Khan 2 (tie), Diya Verma 4, Rohan Gupta 5'''
bx=Table([[Preformatted(rc,code)],[Preformatted(cs,code)]],colWidths=[CW])
bx.setStyle(TableStyle([("BOX",(0,0),(-1,-1),0.5,colors.black),("LINEBELOW",(0,0),(0,0),0.3,colors.grey),("BACKGROUND",(0,0),(-1,-1),colors.HexColor("#F7F7F7")),("TOPPADDING",(0,0),(-1,-1),3),("BOTTOMPADDING",(0,0),(-1,-1),3)]))
S.append(bx)
S+=H2("<b>Results</b>")
S+=[B("<b>Achieved:</b> complete SDLC documentation (problem statement, SRS, 15 diagrams), a working result-processing prototype and a normalised database."),
B("<b>Accuracy:</b> all 15 test cases pass (9 unit, 6 integration). Two faults were injected on purpose: changing the pass check from \u2265 to &gt; was caught by TC03 and TC14, and changing the rounding rule from half-up to half-even was caught by TC06. Percentages use exact decimal arithmetic, rounded to 2 places."),
B(f"<b>Estimate:</b> UFP {E['ufp']} (8 inputs, 5 outputs, 4 enquiries, 5 internal files, 1 external file; average weights), VAF {E['vaf']:.2f}, FP {E['fp']:.2f} = {E['pm']:.2f} person-months at 10 FP per person-month (an assumed productivity)."),
B(f"<b>Schedule:</b> expected duration {endw:.1f} weeks on the critical path (standard deviation {E['sd']:.2f} weeks); 95% confidence of finishing within {p95:.1f} weeks.")]
S+=H2("<b>Conclusion</b>")
S.append(P("<b>Learning outcomes:</b> applying the SDLC, writing an SRS, drawing function-oriented, ER and UML models, unit and integration testing with Python unittest, Function Point estimation and project scheduling. "
"<b>Summary:</b> SRMS removes manual calculation errors, applies one grading rule everywhere and lets a wrong mark be corrected with the result and ranks updated automatically; every design decision can be traced from the requirements to the code and tests."))
S+=H2("<b>Future Scope</b>")
S.append(P("Web and mobile front end with role-based login, parent portal and SMS / e-mail result notification, PDF report cards, board-specific grading templates, grace marks and supplementary exams, and a cloud-hosted analytics dashboard."))
S+=H2("<b>Mapped SDG</b>")
S.append(P("SDG 4 Quality Education (accurate and timely feedback on learning); SDG 9 Industry, Innovation and Infrastructure (digital tools for schools); SDG 12 Responsible Consumption and Production (digital report cards reduce paper)."))
qr=RLImage("figs/qr.png",width=26*mm,height=26*mm)
gh=Table([[ [P("<b>GitHub Repository</b>",h2),B("Project Link: https://github.com/RishabhGupta06/school-result-management-system"),
            P("<b>QR Code (Scanner for GitHub)</b>",h2),B("Scan the QR code on the right with a phone camera to open the repository: source code, SQL schema, tests, SRS and all diagrams.")],qr]],colWidths=[CW-32*mm,30*mm])
gh.setStyle(TableStyle([("VALIGN",(0,0),(-1,-1),"TOP"),("LEFTPADDING",(0,0),(-1,-1),0)])); S.append(KeepTogether(gh))
ins=ParagraphStyle("ins",parent=body,fontSize=8,leading=9.5,textColor=colors.HexColor("#444444"))
S+=[P("<b>Instructions (Do Not Delete)</b>",ParagraphStyle("i",parent=ins,fontName="Times-Bold",spaceBefore=3)),
P("Keep submission strictly 2-3 pages. Font: Times New Roman / Calibri (11\u201312 pt). Headings bold, content concise. Ensure GitHub link is working. QR code must scan correctly.",ins)]
doc.build(S)
