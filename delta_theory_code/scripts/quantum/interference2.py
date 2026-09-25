import numpy as np
def build(L1,L2):
    edges=[]; n=2; a=[0]+list(range(n,n+L1)); n+=L1; b=[0]+list(range(n,n+L2)); n+=L2; R=n; n+=1
    for p in (a,b):
        for u,v in zip(p,p[1:]): edges.append((u,v))
        edges.append((p[-1],R))
    edges.append((0,1))
    # greedy edge colouring: each colour is a set of relations sharing no part (one encounter per part per tick)
    col={}; 
    for e in edges:
        used={col[f] for f in col if set(f)&set(e)}
        c=0
        while c in used: c+=1
        col[e]=c
    return n,R,edges,col
def run(L1,L2,T=8000,amp=0.02):
    n,R,edges,col=build(L1,L2); C=max(col.values())+1
    tau=np.ones(n); dl=np.ones(n)
    tau[0]*=1+amp; dl[0]*=1-amp; tau[1]*=1-amp; dl[1]*=1+amp
    rec={}
    for (u,v) in edges: rec[(u,v)]=dl[v]; rec[(v,u)]=dl[u]
    th=[]; thS=[]
    for t in range(T):
        for (u,v) in edges:
            if col[(u,v)]!=t%C: continue
            du,dv=dl[u],dl[v]
            F=tau[u]*rec[(u,v)]-tau[v]*rec[(v,u)]          # each side registers the other as it was at their last contact
            Tt=tau[u]+tau[v]; Dd=du+dv
            dl[u]+=F/Tt; dl[v]-=F/Tt; tau[u]-=F/Dd; tau[v]+=F/Dd
            rec[(u,v)]=dv; rec[(v,u)]=du
        if (tau<=0).any() or (dl<=0).any(): return None,None,C
        th.append(0.5*np.log(tau[R]/dl[R])); thS.append(0.5*np.log(tau[0]/dl[0]))
    return np.array(th),np.array(thS),C
print("one encounter per part per tick (edge colouring), latency = age of the record from the last contact")
for L2 in range(3,11):
    th,thS,C=run(3,L2)
    if th is None: print(f"  paths 3 and {L2}: positivity broke"); continue
    h=len(th)//2
    print(f"  paths 3 and {L2} (difference {L2-3}): receiver oscillation {th[h:].std():.5f} | source oscillation {thS[h:].std():.5f} (early {thS[:500].std():.5f}) | colours {C}")
