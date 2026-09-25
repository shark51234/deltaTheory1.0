import numpy as np, random, sys
from collections import deque
class World:
    def __init__(s,N0,seed,cap=60000):
        s.r=np.random.default_rng(seed); random.seed(seed)
        s.t=np.zeros(cap); s.d=np.zeros(cap); s.alive=np.zeros(cap,bool); s.uid=np.zeros(cap,dtype=np.int64)
        s.nb=[set() for _ in range(cap)]; s.free=list(range(cap-1,-1,-1)); s.e=0; s.nuid=0
        t=s.r.uniform(.2,1.8,N0); d=s.r.uniform(.2,1.8,N0); t/=t.sum(); d/=d.sum()
        ks=[s.new(a,b) for a,b in zip(t,d)]
        for x in range(N0): s.link(ks[x],ks[(x+1)%N0])
    def new(s,t,d):
        k=s.free.pop(); s.t[k]=t; s.d[k]=d; s.alive[k]=True; s.nb[k]=set(); s.uid[k]=s.nuid; s.nuid+=1; return k
    def link(s,a,b):
        if a!=b: s.nb[a].add(b); s.nb[b].add(a)
    def eta(s,k): return np.sqrt(s.t[k]*s.d[k])
    def choose(s):
        idx=np.flatnonzero(s.alive); i=int(idx[s.r.integers(len(idx))]); nb=list(s.nb[i])
        if not nb: return i,None
        thi=0.5*np.log(s.t[i]/s.d[i])
        j=random.choices(nb,weights=[np.exp(thi-0.5*np.log(s.t[m]/s.d[m])) for m in nb])[0]
        return i,j
    def apply(s,i,j):
        ti,di,tj,dj=s.t[i],s.d[i],s.t[j],s.d[j]; ei,ej=s.eta(i),s.eta(j)
        rec=dict(mass=abs(np.log(ei/ej)),motion=abs(0.5*np.log(ti/di)-0.5*np.log(tj/dj)),
                 degmax=max(len(s.nb[i]),len(s.nb[j])),share=max(ei,ej))
        kids=[]; ui,uj=int(s.uid[i]),int(s.uid[j]); inherited=0
        if (ti-tj)*(di-dj)<=0:
            rec['chan']='relations dominate (spacelike)'
            if random.random()<di/(di+dj):
                s.t[i],s.d[i]=ti,(di+dj)/2; s.t[j],s.d[j]=tj/2,dj/2; c=s.new(tj/2,di/2)
            else:
                s.t[j],s.d[j]=tj,(di+dj)/2; s.t[i],s.d[i]=ti/2,di/2; c=s.new(ti/2,dj/2)
            s.link(c,i); s.link(c,j); kids=[c]; rec['out']='two-view birth'
            after=s.eta(i)+s.eta(j)+s.eta(c)
        else:
            rec['chan']='selves dominate (timelike)'; dom,sub=(i,j) if ti>tj else (j,i)
            if random.random()<s.d[dom]/(s.d[dom]+s.d[sub]):
                s.t[dom]+=s.t[sub]; s.d[dom]+=s.d[sub]
                for m in list(s.nb[sub]):
                    s.nb[m].discard(sub)
                    if m!=dom and m not in s.nb[dom]: s.link(dom,m); inherited+=1
                s.nb[sub]=set(); s.alive[sub]=False; s.free.append(sub)
                rec['out']='absorption'; after=s.eta(dom)
            else:
                tD,dD,tS,dS=s.t[dom],s.d[dom],s.t[sub],s.d[sub]
                s.t[dom],s.d[dom],s.t[sub],s.d[sub]=tD/2,dD/2,tS/2,dS/2
                for (a,b) in ((tD/2,dS/2),(tS/2,dD/2)):
                    c=s.new(a,b); s.link(c,dom); s.link(c,sub); kids.append(c)
                rec['out']='crossover birth'; after=s.eta(dom)+s.eta(sub)+sum(s.eta(c) for c in kids)
        rec['dmass']=(after-(ei+ej))/(ei+ej)       # relative mass change: + motion became mass, - mass became motion
        rec['inherited']=inherited
        s.e+=1
        return rec,ui,uj,[int(s.uid[c]) for c in kids]
def bfs_uid(w,sources):
    dist={}; dq=deque()
    for k in sources: dist[k]=0; dq.append(k)
    while dq:
        u=dq.popleft()
        for v in w.nb[u]:
            if v not in dist: dist[v]=dist[u]+1; dq.append(v)
    return {int(w.uid[k]):dd for k,dd in dist.items()}
if __name__=="__main__":
    seed=int(sys.argv[1]); WARM=15000; K=int(sys.argv[2]) if len(sys.argv)>2 else 1500; RUN=K+int(sys.argv[3]) if len(sys.argv)>3 else 20000; EVERY=int(sys.argv[4]) if len(sys.argv)>4 else 20
    w=World(200,seed)
    for _ in range(WARM):
        i,j=w.choose()
        if j is not None: w.apply(i,j)
        else: w.e+=1
    tracers=[]; done=[]; recs=[]
    for n in range(RUN):
        i,j=w.choose()
        if j is None: w.e+=1; continue
        start = (n%EVERY==0)
        if start: dist=bfs_uid(w,[i,j])
        rec,ui,uj,kids=w.apply(i,j); recs.append(rec)
        for T in tracers:
            if ui in T['inf'] or uj in T['inf']:
                T['inf'].add(ui); T['inf'].add(uj); T['inf'].update(kids)
        if start: tracers.append(dict(t0=w.e,chan=rec['chan'],out=rec['out'],dist=dist,inf={ui,uj,*kids}))
        for T in list(tracers):
            if w.e-T['t0']>=K:
                reached=[T['dist'][u] for u in T['inf'] if u in T['dist']]
                done.append(dict(chan=T['chan'],out=T['out'],reach=float(np.mean(reached)),far=int(max(reached)),count=len(T['inf'])))
                tracers.remove(T)
    import json; json.dump(dict(recs=recs,done=done),open(f"ch_{seed}.json","w"))
    print(f"seed {seed}: {len(recs)} encounters logged, {len(done)} tracers finished")
