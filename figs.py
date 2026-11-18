import subprocess, json, textwrap
import graphviz as gv
E=json.load(open("est.json"))
F="Helvetica"
FILL={"f01","f03","f04","f05","f08","f15"}
def render(g,name,dpi=170):
    g.graph_attr.update(dpi=str(dpi),fontname=F,pad="0.15")
    if name in FILL: g.graph_attr.update(size="6.2,5.4!",ratio="fill")
    g.node_attr.setdefault("fontname",F); g.edge_attr.setdefault("fontname",F)
    g.render(f"figs/{name}",format="png",cleanup=True)
BLUE,YEL,GRN,RED,GRY="#DCE9F7","#FFF2CC","#D9EAD3","#F4CCCC","#EEEEEE"

# 1 flowchart
g=gv.Digraph(graph_attr=dict(rankdir="TB",nodesep="0.3",ranksep="0.22"),node_attr=dict(fontsize="11",style="filled",fillcolor="white"))
g.node("s","Start",shape="box",style="rounded,filled",fillcolor=BLUE)
g.node("l","Login (Admin / Teacher)",shape="box")
g.node("d1","Valid\ncredentials?",shape="diamond",fillcolor=YEL)
g.node("x1","Show error",shape="box",fillcolor=RED)
g.node("em","Select class, exam, subject;\nenter student marks",shape="box")
g.node("d2","Marks 0 to\nmaximum?",shape="diamond",fillcolor=YEL)
g.node("x2","Reject entry",shape="box",fillcolor=RED)
g.node("sv","Save marks to database",shape="box")
g.node("cal","Compute total, %, grade,\nPASS / FAIL, ranks",shape="box")
g.node("rc","Generate report card\nand class summary",shape="box")
g.node("e","End",shape="box",style="rounded,filled",fillcolor=BLUE)
for a,b in [("s","l"),("l","d1"),("em","d2"),("sv","cal"),("cal","rc"),("rc","e")]: g.edge(a,b)
g.edge("d1","x1",label=" No",fontsize="10"); g.edge("x1","l")
g.edge("d1","em",label=" Yes",fontsize="10")
g.edge("d2","x2",label=" No",fontsize="10"); g.edge("x2","em")
g.edge("d2","sv",label=" Yes",fontsize="10")
render(g,"f01")

# 2 use case
g=gv.Digraph(graph_attr=dict(rankdir="LR",nodesep="0.18",ranksep="1.2",compound="true"),node_attr=dict(fontsize="11"))
for a in ["Admin","Teacher","Student / Parent"]:
    g.node(a,a+"\n«actor»",shape="box",style="filled",fillcolor=GRY)
with g.subgraph(name="cluster_s") as c:
    c.attr(label="School Result Management System",style="rounded",fontsize="12",fontname=F)
    ucs=["Login","Manage Students","Manage Classes\n& Subjects","Manage Teachers","Enter Marks","Update Marks\n(correction)",
         "Calculate Result","Generate Report Card","Publish Results","View Result","View Class Analysis","Download Report Card"]
    for u in ucs: c.node(u,u,shape="ellipse",style="filled",fillcolor="white")
A={"Admin":["Login","Manage Students","Manage Classes\n& Subjects","Manage Teachers","Publish Results","View Class Analysis"],
   "Teacher":["Login","Enter Marks","Update Marks\n(correction)","Generate Report Card","View Class Analysis"],
   "Student / Parent":["Login","View Result","Download Report Card"]}
for a,us in A.items():
    for u in us: g.edge(a,u,arrowhead="none")
g.edge("Generate Report Card","Calculate Result",label="«include»",style="dashed",fontsize="9")
g.edge("Update Marks\n(correction)","Enter Marks",label="«extend»",style="dashed",fontsize="9")
g.edge("View Result","Calculate Result",label="«include»",style="dashed",fontsize="9")
render(g,"f02")

# 3 DFD level-1
g=gv.Digraph(graph_attr=dict(rankdir="TB",nodesep="0.3",ranksep="0.55"),node_attr=dict(fontsize="13"))
for n in ["ADMIN","TEACHER","STUDENT"]: g.node(n,n,shape="box",style="filled",fillcolor=GRY)
for i,t in enumerate(["Manage\nMaster Data","Enter\nMarks","Calculate\nResult","Generate\nReports","Publish /\nView Results"],1):
    g.node(f"P{i}",f"{i}.0\n{t}",shape="circle",style="filled",fillcolor=BLUE,width="1.0")
for i,t in enumerate(["Students","Classes & Subjects","Marks","Results"],1):
    g.node(f"D{i}",f"D{i}  {t}",shape="box",style="filled",fillcolor=YEL,peripheries="1")
E_=[("ADMIN","P1","master data"),("P1","D1",""),("P1","D2",""),("TEACHER","P2","marks"),("D1","P2","student list"),("D2","P2","subject max"),
("P2","D3","valid marks"),("D3","P3","marks"),("D2","P3","max marks"),("P3","D4","result, grade"),("D4","P4","results"),("D1","P4","names"),
("P4","TEACHER","report card, summary"),("ADMIN","P5","publish"),("D4","P5","published results"),("P5","STUDENT","result / report card"),("STUDENT","P5","view request")]
for a,b,l in E_: g.edge(a,b)
render(g,"f03")

# 4 structure chart
g=gv.Digraph(graph_attr=dict(rankdir="LR",nodesep="0.08",ranksep="0.45"),node_attr=dict(shape="box",fontsize="9",style="filled",fillcolor="white",margin="0.06,0.03"))
g.node("M","SRMS Main",fillcolor=BLUE,fontsize="11")
tree={"Manage Master\nData":["Add Class","Add Student","Add Subject"],"Enter Marks":["Validate Marks","Save Marks"],
"Calculate\nResult":["Total &\nPercentage","Assign Grade","Check Subject\nPass / Fail","Assign Ranks"],
"Generate\nReports":["Report Card","Class Summary","Rank List"],"Publish &\nView":["Publish Result","Student View"]}
for k,(p,cs) in enumerate(tree.items()):
    g.node(f"p{k}",p,fillcolor=YEL,fontsize="10"); g.edge("M",f"p{k}",arrowsize="0.6")
    for j,c in enumerate(cs):
        g.node(f"c{k}{j}",c); g.edge(f"p{k}",f"c{k}{j}",arrowsize="0.6")
render(g,"f04")

# 5 ER
g=gv.Digraph(graph_attr=dict(rankdir="TB",nodesep="0.3",ranksep="0.55"),node_attr=dict(fontsize="13"))
def ent(n,rows):
    r="".join(f'<TR><TD ALIGN="LEFT">{x}</TD></TR>' for x in rows)
    g.node(n,f'<<TABLE BORDER="1" CELLBORDER="0" CELLSPACING="0" BGCOLOR="{BLUE}"><TR><TD BGCOLOR="#9DB9DF"><B>{n}</B></TD></TR>{r}</TABLE>>',shape="plaintext")
ent("CLASS",["<U>class_id</U>","name"])
ent("STUDENT",["<U>student_id</U>","roll_no","name","class_id (FK)"])
ent("SUBJECT",["<U>subject_id</U>","name","max_marks"])
ent("TEACHER",["<U>teacher_id</U>","name","username","role"])
ent("EXAM",["<U>exam_id</U>","name","year"])
def rel(n,l): g.node(n,l,shape="diamond",style="filled",fillcolor=YEL,fontsize="9")
rel("r1","enrolled in"); rel("r2","includes"); rel("r3","teaches"); rel("r4","scores")
g.edge("CLASS","r1",label="1",fontsize="9",arrowhead="none"); g.edge("r1","STUDENT",label="N",fontsize="9",arrowhead="none")
g.edge("CLASS","r2",label="M",fontsize="9",arrowhead="none"); g.edge("r2","SUBJECT",label="N",fontsize="9",arrowhead="none")
g.edge("TEACHER","r3",label="1",fontsize="9",arrowhead="none"); g.edge("r3","r2",label="N (class_subject)",fontsize="8",arrowhead="none",style="dashed")
g.edge("STUDENT","r4",label="M",fontsize="9",arrowhead="none"); g.edge("r4","SUBJECT",label="N",fontsize="9",arrowhead="none"); g.edge("r4","EXAM",label="P  (marks)",fontsize="9",arrowhead="none")
render(g,"f05")

# 6 class diagram
g=gv.Digraph(graph_attr=dict(rankdir="TB",nodesep="0.35",ranksep="0.6"),node_attr=dict(fontsize="12"))
def cls(n,attrs,meths,fill="white"):
    a="<BR ALIGN='LEFT'/>".join(attrs)+"<BR ALIGN='LEFT'/>" if attrs else " "; m="<BR ALIGN='LEFT'/>".join(meths)+"<BR ALIGN='LEFT'/>" if meths else " "
    g.node(n,f'<<TABLE BORDER="1" CELLBORDER="1" CELLSPACING="0" BGCOLOR="{fill}"><TR><TD><B>{n}</B></TD></TR><TR><TD ALIGN="LEFT" BALIGN="LEFT">{a}</TD></TR><TR><TD ALIGN="LEFT" BALIGN="LEFT">{m}</TD></TR></TABLE>>',shape="plaintext")
cls("User",["- username"],["+ login()"])
cls("Admin",[],["+ publishResult()"]); cls("Teacher",[],["+ enterMarks()","+ updateMarks()"])
cls("SchoolClass",["- name"],["+ addStudent()"]); cls("Student",["- roll_no","- name"],["+ viewResult()"])
cls("Subject",["- name","- max_marks"],[]); cls("Exam",["- name","- year"],[])
cls("MarkEntry",["- marks"],["+ validate()"])
cls("ResultService",[],["+ result()","+ classRanks()","+ reportCard()"],YEL)
cls("Grading",[],["+ percentage()","+ gradeFor()","+ subjectPassed()","+ assignRanks()"],YEL)
for a in ["Admin","Teacher"]: g.edge(a,"User",arrowhead="empty")
g.edge("SchoolClass","Student",arrowhead="odiamond",headlabel="*",taillabel="1",labeldistance="1.6",fontsize="10")
for n in ["Student","Subject","Exam"]: g.edge(n,"MarkEntry",arrowhead="none",taillabel="1",headlabel="*",labeldistance="1.6",fontsize="10")
g.edge("Teacher","MarkEntry",label=" enters",style="dashed",arrowhead="vee",fontsize="10")
g.edge("ResultService","MarkEntry",label=" reads",style="dashed",arrowhead="vee",fontsize="10")
g.edge("ResultService","Grading",label=" uses",style="dashed",arrowhead="vee",fontsize="10")
{ g.edge("User","SchoolClass",style="invis") }
render(g,"f06")

# 7 object diagram
g=gv.Digraph(graph_attr=dict(rankdir="TB",nodesep="0.25",ranksep="0.5"),node_attr=dict(fontsize="9"))
def obj(n,title,rows):
    r="".join(f'<TR><TD ALIGN="LEFT">{x}</TD></TR>' for x in rows)
    g.node(n,f'<<TABLE BORDER="1" CELLBORDER="0" CELLSPACING="0" BGCOLOR="white"><TR><TD BGCOLOR="{BLUE}"><U>{title}</U></TD></TR>{r}</TABLE>>',shape="plaintext")
obj("c1","c1 : SchoolClass",["name = \"X-A\""]); obj("e1","e1 : Exam",["name = \"Annual 2026\""])
obj("s1","s1 : Student",["roll_no = \"01\"","name = \"Aarav Sharma\""])
obj("r1","r1 : Result",["total = 434 / 500","percent = 86.80","grade = \"A\"","result = PASS","rank = 2"])
obj("m1","m1 : MarkEntry",["subject = Maths","marks = 94"]); obj("m2","m2 : MarkEntry",["subject = Science","marks = 91"]); obj("m3","m3 : MarkEntry",["subject = English","marks = 88"])
g.edge("c1","s1",label="has",arrowhead="none",fontsize="8"); g.edge("s1","r1",label="gets",arrowhead="none",fontsize="8"); g.edge("e1","r1",label="for",arrowhead="none",fontsize="8")
for m in ["m1","m2","m3"]: g.edge("s1",m,label="scored",arrowhead="none",fontsize="8")
render(g,"f07")

# 8 state chart
g=gv.Digraph(graph_attr=dict(rankdir="TB",nodesep="0.5",ranksep="0.45"),node_attr=dict(fontsize="10",shape="box",style="rounded,filled",fillcolor=BLUE))
g.node("i","",shape="circle",width="0.18",style="filled",fillcolor="black"); g.node("f","",shape="doublecircle",width="0.18",style="filled",fillcolor="black")
for n in ["Draft","Submitted","Verified","Published","Under\nCorrection"]: g.node(n,n)
g.edge("i","Draft"); g.edge("Draft","Submitted",label="teacher submits\n[all marks valid]",fontsize="8")
g.edge("Submitted","Verified",label="admin verifies",fontsize="8"); g.edge("Submitted","Draft",label="rejected",fontsize="8")
g.edge("Verified","Published",label="publish",fontsize="8"); g.edge("Published","Under\nCorrection",label="correction\nrequest",fontsize="8")
g.edge("Under\nCorrection","Verified",label="marks updated",fontsize="8"); g.edge("Published","f",label="academic year\nclosed",fontsize="8")
render(g,"f08")

# 9 activity (swimlanes)
g=gv.Digraph(graph_attr=dict(rankdir="TB",nodesep="0.25",ranksep="0.28",newrank="true"),node_attr=dict(fontsize="9",shape="box",style="rounded,filled",fillcolor="white"))
def lane(n,label,nodes):
    with g.subgraph(name=f"cluster_{n}") as c:
        c.attr(label=label,style="filled",fillcolor="#FAFAFA",fontsize="11",fontname=F)
        for k,v in nodes: c.node(k,v)
lane("t","Teacher",[("t1","Login"),("t2","Enter marks"),("t3","Submit mark sheet")])
lane("s","System",[("s1","Validate marks"),("s2","Save marks"),("s3","Compute result\n& ranks"),("s5","Generate\nreport cards"),("s6","Update\nclass summary")])
lane("a","Admin",[("a1","Verify results"),("a2","Publish results")])
g.node("st","",shape="circle",width="0.15",style="filled",fillcolor="black"); g.node("en","",shape="doublecircle",width="0.15",style="filled",fillcolor="black")
g.node("d","valid?",shape="diamond",fillcolor=YEL); g.node("fk","",shape="box",height="0.05",width="1.2",style="filled",fillcolor="black"); g.node("jn","",shape="box",height="0.05",width="1.2",style="filled",fillcolor="black")
g.edge("st","t1");g.edge("t1","t2");g.edge("t2","s1");g.edge("s1","d");g.edge("d","t2",label="no",fontsize="8");g.edge("d","s2",label="yes",fontsize="8")
g.edge("s2","t3");g.edge("t3","s3");g.edge("s3","a1");g.edge("a1","a2");g.edge("a2","fk");g.edge("fk","s5");g.edge("fk","s6");g.edge("s5","jn");g.edge("s6","jn");g.edge("jn","en")
render(g,"f09")

# 11 collaboration
g=gv.Digraph(engine="circo",graph_attr=dict(splines="true",mindist="1.6"),node_attr=dict(fontsize="12",shape="box",style="filled",fillcolor=BLUE))
for n in ["Teacher","UI","ResultService","Grading","Database"]: g.node(n,n)
for a,b,l in [("Teacher","UI","1: enterMarks()"),("UI","ResultService","2: enter_marks(...)"),("ResultService","Grading","3: validate_marks()"),
("ResultService","Database","4: INSERT marks"),("UI","ResultService","5: result(student, exam)"),("ResultService","Database","6: SELECT marks"),
("ResultService","Grading","7: percentage(), grade_for(), subject_passed()"),("ResultService","UI","8: result dict"),("UI","Teacher","9: show result")]:
    g.edge(a,b,label=l,fontsize="10")
render(g,"f11")

# 12 component
g=gv.Digraph(graph_attr=dict(rankdir="TB",nodesep="0.3",ranksep="0.45"),node_attr=dict(shape="component",fontsize="10",style="filled"))
g.node("ui","Web / Desktop UI\n(login, marks entry, reports)",fillcolor=BLUE)
for k,t in [("auth","Auth Manager"),("stu","Student & Class\nManager"),("mk","Marks Manager\n(validation)"),("eng","Result Engine\n(grading rules)"),("rep","Report Generator\n(report card, PDF)")]:
    g.node(k,t,fillcolor=YEL)
g.node("da","Data Access Layer",fillcolor=GRN); g.node("db","Database\n(SQLite prototype / MySQL)",shape="cylinder",fillcolor=GRY)
for k in ["auth","stu","mk","eng","rep"]: g.edge("ui",k)
g.edge("mk","eng",style="dashed",label="uses",fontsize="8"); g.edge("rep","eng",style="dashed",label="uses",fontsize="8")
for k in ["auth","stu","mk","eng","rep"]: g.edge(k,"da")
g.edge("da","db")
render(g,"f12")

# 13 deployment
g=gv.Digraph(graph_attr=dict(rankdir="TB",nodesep="0.35",ranksep="0.6"),node_attr=dict(shape="box3d",fontsize="10",style="filled"))
g.node("t","Teacher PC\n«device»\nBrowser: marks entry",fillcolor=BLUE); g.node("a","Admin PC\n«device»\nBrowser: admin console",fillcolor=BLUE); g.node("p","Student / Parent\nPhone or PC\n«device»\nBrowser: view result",fillcolor=BLUE)
g.node("app","Application Server\n«node»\nSRMS modules\n(auth, marks, result, reports)",fillcolor=YEL)
g.node("db","Database Server\n«node»\nMySQL (results DB)",fillcolor=GRN); g.node("pr","Printer / PDF export\n«device»",fillcolor=GRY)
for n in "tap": g.edge(n,"app",label="HTTPS",fontsize="8")
g.edge("app","db",label="TCP/IP 3306",fontsize="8"); g.edge("app","pr",label="print / export",fontsize="8")
render(g,"f13")

# 15 PERT
T,te,ES,EF,sl,crit=E["T"],E["te"],E["ES"],E["EF"],E["slack"],E["crit"]
FILL.discard("f15")
g=gv.Digraph(graph_attr=dict(rankdir="LR",nodesep="0.12",ranksep="0.3"),node_attr=dict(shape="plaintext",fontsize="12"))
for k,v in T.items():
    col="#F4CCCC" if k in crit else "white"
    g.node(k,f'<<TABLE BORDER="1" CELLBORDER="1" CELLSPACING="0" BGCOLOR="{col}"><TR><TD COLSPAN="2"><B>{k}</B> ({te[k]:.1f})</TD></TR><TR><TD>{ES[k]:.1f}</TD><TD>{EF[k]:.1f}</TD></TR></TABLE>>')
    for p in v[1]: g.edge(p,k,color="#B00020" if (k in crit and p in crit) else "black",penwidth="2.2" if (k in crit and p in crit) else "1",arrowsize="0.7")
render(g,"f15")
print("ok")
