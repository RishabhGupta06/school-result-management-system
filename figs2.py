import json, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
E=json.load(open("est.json"))
# ---- Fig 10 sequence diagram ----
fig,ax=plt.subplots(figsize=(6.4,5.4)); ax.set_xlim(0,10); ax.set_ylim(0,10.4); ax.axis("off")
names=["Teacher","UI","ResultService","Grading","Database"]; xs=[1,3.2,5.4,7.2,9.2]
for n,x in zip(names,xs):
    ax.add_patch(Rectangle((x-0.85,9.55),1.7,0.65,fc="#DCE9F7",ec="k",lw=0.8)); ax.text(x,9.87,n,ha="center",va="center",fontsize=8.5)
    ax.plot([x,x],[0.2,9.55],ls="--",c="gray",lw=0.7)
def msg(i,j,y,t,dash=False):
    ax.annotate("",xy=(xs[j],y),xytext=(xs[i],y),arrowprops=dict(arrowstyle="->",lw=0.9,ls="--" if dash else "-"))
    ax.text((xs[i]+xs[j])/2,y+0.12,t,ha="center",va="bottom",fontsize=7)
msg(0,1,9.0,"1: enterMarks(student, subject, exam, marks)")
msg(1,2,8.4,"2: enter_marks(...)")
msg(2,3,7.8,"3: validate_marks(marks, max)")
msg(3,2,7.3,"valid / ValueError",True)
ax.add_patch(Rectangle((0.3,5.0),9.6,2.0,fc="none",ec="#555",lw=0.8)); ax.text(0.4,6.8,"alt  [marks valid]",fontsize=7,va="center",weight="bold")
msg(2,4,6.3,"4: INSERT INTO marks")
msg(4,2,5.7,"saved (UNIQUE / CHECK passed)",True)
msg(2,1,5.2,"5: success",True)
ax.plot([0.3,9.9],[4.75,4.75],c="#555",lw=0.8,ls=":"); 
ax.add_patch(Rectangle((0.3,4.0),9.6,0.75,fc="none",ec="#555",lw=0.8)); ax.text(0.4,4.55,"[else]",fontsize=7,weight="bold"); msg(2,1,4.2,"5': error message (marks out of range)",True)
msg(0,1,3.4,"6: viewResult(student, exam)")
msg(1,2,2.9,"7: result(student, exam)")
msg(2,4,2.4,"8: SELECT marks, max_marks")
msg(2,3,1.8,"9: percentage(), grade_for(), subject_passed()")
msg(2,1,1.2,"10: result (total, %, grade, PASS/FAIL)",True)
msg(1,0,0.6,"11: show result",True)
fig.savefig("figs/f10.png",dpi=200,bbox_inches="tight",facecolor="white"); plt.close(fig)
# ---- Fig 14 gantt ----
T,ES,te,crit,end=E["T"],E["ES"],E["te"],E["crit"],E["end"]
fig,ax=plt.subplots(figsize=(6.6,3.7))
keys=list(T)
for i,k in enumerate(keys):
    c="#222" if k in crit else "#9AA5B1"
    ax.barh(len(keys)-1-i,te[k],left=ES[k],color=c,height=0.55)
    if E["slack"][k]>0.01: ax.barh(len(keys)-1-i,E["slack"][k],left=ES[k]+te[k],color="none",edgecolor="#777",hatch="///",height=0.55,lw=0.5)
ax.set_yticks(range(len(keys))); ax.set_yticklabels([f"{k}  {T[k][0]}" for k in reversed(keys)],fontsize=7)
ax.set_xlabel("Project week",fontsize=8); ax.set_xticks(range(0,21,2)); ax.tick_params(axis="x",labelsize=7); ax.grid(axis="x",lw=0.3)
ms=[(5,"M1 Design done"),(10.17,"M2 Modules done"),(16.33,"M3 Integrated"),(end,"M4 Go-live")]
for x,l in ms:
    ax.axvline(x,color="#B00020",lw=0.8,ls="--"); ax.text(x,len(keys)-0.1,l,rotation=0,fontsize=6.5,ha="center",va="bottom",color="#B00020")
ax.set_ylim(-0.6,len(keys)+0.6)
from matplotlib.lines import Line2D
ax.legend(handles=[Rectangle((0,0),1,1,fc="#222"),Rectangle((0,0),1,1,fc="#9AA5B1"),Rectangle((0,0),1,1,fc="none",ec="#777",hatch="///")],labels=["Critical activity","Non-critical","Slack (float)"],fontsize=6.5,loc="lower left")
for s in ["top","right"]: ax.spines[s].set_visible(False)
fig.savefig("figs/f14.png",dpi=200,bbox_inches="tight",facecolor="white"); plt.close(fig)
# ---- Fig 9 swimlane activity (matplotlib) ----
fig,ax=plt.subplots(figsize=(6.0,5.6)); ax.set_xlim(0,9); ax.set_ylim(0,11); ax.axis("off")
lanes=[("Teacher",0,3),("System",3,6),("Admin",6,9)]
for n,a,b in lanes:
    ax.add_patch(Rectangle((a,0),b-a,10.2,fc="#FAFAFA",ec="k",lw=0.8)); ax.add_patch(Rectangle((a,10.2),b-a,0.7,fc="#DCE9F7",ec="k",lw=0.8)); ax.text((a+b)/2,10.55,n,ha="center",va="center",fontsize=9,weight="bold")
def box(x,y,t,fc="white",w=2.1,h=0.7):
    ax.add_patch(Rectangle((x-w/2,y-h/2),w,h,fc=fc,ec="k",lw=0.8,joinstyle="round")); ax.text(x,y,t,ha="center",va="center",fontsize=7.2)
def dia(x,y,t):
    ax.add_patch(plt.Polygon([(x,y+0.55),(x+1.0,y),(x,y-0.55),(x-1.0,y)],fc="#FFF2CC",ec="k",lw=0.8)); ax.text(x,y,t,ha="center",va="center",fontsize=7)
def arr(x1,y1,x2,y2,t=None):
    ax.annotate("",xy=(x2,y2),xytext=(x1,y1),arrowprops=dict(arrowstyle="->",lw=0.9)); 
    if t: ax.text((x1+x2)/2+0.08,(y1+y2)/2+0.08,t,fontsize=6.5)
ax.add_patch(plt.Circle((1.5,9.85),0.15,fc="k")); 
box(1.5,9.0,"Login"); arr(1.5,9.7,1.5,9.35); 
box(1.5,7.7,"Enter marks"); arr(1.5,8.65,1.5,8.05)
dia(4.5,7.7,"Marks valid?"); arr(2.55,7.7,3.5,7.7)
arr(4.5,7.15,4.5,6.6,"yes"); box(4.5,6.25,"Save marks")
ax.plot([4.5,4.5,2.0],[8.25,8.5,8.5],c="k",lw=0.9); ax.annotate("",xy=(2.0,8.05),xytext=(2.0,8.5),arrowprops=dict(arrowstyle="->",lw=0.9)); ax.text(3.0,8.58,"no: correct entry",fontsize=6.5)
box(1.5,5.1,"Submit mark sheet"); arr(3.45,6.25,1.5,5.5); arr(1.5,5.1,4.5,4.4) if False else None
box(4.5,4.3,"Compute result\n& ranks",h=0.8); arr(2.55,5.0,3.45,4.5)
box(7.5,3.3,"Verify results"); arr(5.55,4.1,6.45,3.5)
box(7.5,2.3,"Publish results"); arr(7.5,2.95,7.5,2.65)
ax.add_patch(Rectangle((3.0,1.45),3.0,0.08,fc="k")); arr(6.45,2.3,5.0,1.55)
box(3.6,0.75,"Generate\nreport cards",w=1.6,h=0.7); box(5.4,0.75,"Update class\nsummary",w=1.6,h=0.7)
arr(3.6,1.45,3.6,1.1); arr(5.4,1.45,5.4,1.1)
ax.add_patch(Rectangle((3.0,0.18),3.0,0.08,fc="k")); arr(3.6,0.4,3.6,0.26); arr(5.4,0.4,5.4,0.26)
fig.savefig("figs/f09.png",dpi=200,bbox_inches="tight",facecolor="white"); plt.close(fig)
