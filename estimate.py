import math, json
# ---- Function points (average complexity weights) ----
counts = {"EI":(8,4),"EO":(5,5),"EQ":(4,4),"ILF":(5,10),"EIF":(1,7)}
ufp = sum(n*w for n,w in counts.values())
gsc = [4,3,3,3,3,4,4,3,2,3,2,3,2,3]       # 14 general system characteristics (0-5)
vaf = round(0.65+0.01*sum(gsc),2)
fp = round(ufp*vaf,2)
pm = round(fp/10,2)
print("UFP",ufp,"sum GSC",sum(gsc),"VAF",vaf,"FP",fp,"PM",pm)
# ---- PERT ----
T = {  # id: (name, pred, o, m, p)
"A":("Requirements & SRS",[],1,2,3),
"B":("System design (DFD/UML)",["A"],2,3,4),
"C":("Database design",["B"],1,2,3),
"D":("Student & class module",["C"],2,3,4),
"E":("Marks entry module",["C"],2,3,5),
"F":("Result & grading module",["D","E"],2,3,4),
"G":("Report generation",["F"],1,2,3),
"H":("User interface",["B"],2,3,5),
"I":("Integration",["G","H"],1,1,2),
"J":("Testing",["I"],2,2,3),
"K":("Deployment & training",["J"],1,1,2)}
te={k:(v[2]+4*v[3]+v[4])/6 for k,v in T.items()}
var={k:((v[4]-v[2])/6)**2 for k,v in T.items()}
ES={};EF={}
order=list(T)  # already topological
for k in order:
    ES[k]=max([EF[p] for p in T[k][1]],default=0); EF[k]=ES[k]+te[k]
end=max(EF.values())
LF={};LS={}
for k in reversed(order):
    succ=[s for s in T if k in T[s][1]]
    LF[k]=min([LS[s] for s in succ],default=end); LS[k]=LF[k]-te[k]
slack={k:round(LS[k]-ES[k],2) for k in T}
crit=[k for k in order if abs(slack[k])<1e-9]
sd=math.sqrt(sum(var[k] for k in crit))
from statistics import NormalDist
target=math.ceil(end)+2
prob=NormalDist().cdf((target-end)/sd)
print("te",{k:round(v,2) for k,v in te.items()})
print("ES",{k:round(v,2) for k,v in ES.items()}); print("EF",{k:round(v,2) for k,v in EF.items()})
print("slack",slack); print("critical",crit,"duration",round(end,2),"sigma",round(sd,3),"target",target,"P",round(prob,4))
json.dump(dict(T=T,te=te,ES=ES,EF=EF,slack=slack,crit=crit,end=end,sd=sd,target=target,prob=prob,ufp=ufp,vaf=vaf,fp=fp,pm=pm,gsc=gsc),open("est.json","w"))
