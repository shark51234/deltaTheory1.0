import numpy as np
from interference2 import build
def run(L1,L2,cut=None,T=12000,amp=0.02):
    n,R,edges,col=build(L1,L2); C=max(col.values())+1
    tau=np.ones(n); dl=np.ones(n)
    tau[0]*=1+amp; dl[0]*=1-amp; tau[1]*=1-amp; dl[1]*=1+amp
    rec={}
    for (u,v) in edges: rec[(u,v)]=dl[v]; rec[(v,u)]=dl[u]
    # the relation that delivers each path to the receiver
    endA=[e for e in edges if e[1]==R][0]; endB=[e for e in edges if e[1]==R][1]
    skip={'A':endB,'B':endA}.get(cut)      # 'A' = only path A reaches R; 'B' = only path B reaches R
    th=np.zeros(T); thS=np.zeros(T)
    for t in range(T):
        for (u,v) in edges:
            if col[(u,v)]!=t%C or (u,v)==skip: continue
            du,dv=dl[u],dl[v]; F=tau[u]*rec[(u,v)]-tau[v]*rec[(v,u)]
            Tt=tau[u]+tau[v]; Dd=du+dv; dl[u]+=F/Tt; dl[v]-=F/Tt; tau[u]-=F/Dd; tau[v]+=F/Dd
            rec[(u,v)]=dv; rec[(v,u)]=du
        th[t]=0.5*np.log(tau[R]/dl[R]); thS[t]=0.5*np.log(tau[0]/dl[0])
    return th,thS
def lockin(x,f):
    t=np.arange(len(x)); h=len(x)//3
    return 2*np.mean((x[h:]-x[h:].mean())*np.exp(-2j*np.pi*f*t[h:]))
L1=3
th,thS=run(L1,L1)
s=thS[len(thS)//3:]-thS[len(thS)//3:].mean(); spec=np.abs(np.fft.rfft(s)); fr=np.fft.rfftfreq(len(s))
f0=fr[np.argmax(spec[1:])+1]
print(f"source's dominant frequency: {f0:.4f} cycles per tick (a relation meets every 3 ticks; 1/12 = {1/12:.4f} is a quarter-turn per meeting)")
print(f"{'path difference':>15s} {'|A|':>8s} {'|B|':>8s} {'|both|':>8s} {'|A+B|':>8s} {'phase(B/A)/pi':>14s}")
for L2 in range(L1,L1+13):
    both,_=run(L1,L2); onlyA,_=run(L1,L2,'A'); onlyB,_=run(L1,L2,'B')
    zA,zB,zAB=lockin(onlyA,f0),lockin(onlyB,f0),lockin(both,f0)
    print(f"{L2-L1:15d} {abs(zA):8.5f} {abs(zB):8.5f} {abs(zAB):8.5f} {abs(zA+zB):8.5f} {np.angle(zB/zA)/np.pi:14.3f}")
