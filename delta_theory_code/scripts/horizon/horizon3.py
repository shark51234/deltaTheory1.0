import os as _os_root
_ROOT=_os_root.path.dirname(_os_root.path.dirname(_os_root.path.abspath(__file__)))
import os
import numpy as np, random, sys, json
from collections import deque
sys.path.insert(0,os.path.join(_ROOT,'space'))
from space import World
def run(seed,Nw,K,S=80,burn=8000,every=4000):
    w=World(seed,'pair',cap=80000)
    while 2<=len(w.alive_list)<Nw: w.step()
    if len(w.alive_list)<Nw: return None
    cap=len(w.t); uid=np.full(cap,-1,dtype=np.int64); nuid=[0]
    for k in w.alive_list: uid[k]=nuid[0]; nuid[0]+=1
    kt=np.full((cap,S),-1.0); klt=np.zeros((cap,S)); kld=np.zeros((cap,S))
    rng=np.random.default_rng(seed); src=[None]*S; suid=np.full(S,-2,dtype=np.int64)
    def own(k,now):
        for s in np.flatnonzero(suid==uid[k]): kt[k,s]=now; klt[k,s]=np.log(w.t[k]); kld[k,s]=np.log(w.d[k])
    def pick_source(s,now):
        nodes=w.alive_list; eta=np.sqrt(w.t[nodes]*w.d[nodes]); tot=eta.sum()
        while True:
            k=nodes[rng.integers(len(nodes))]
            if np.sqrt(w.t[k]*w.d[k])<=0.01*tot: break
        src[s]=k; suid[s]=uid[k]; kt[:,s]=-1.0; own(k,now)
    for s in range(S): pick_source(s,0.0)
    born=[]; orig=w.new
    def hook(t,d):
        k=orig(t,d); born.append(k); return k
    w.new=hook; samples={}; know={}; thr_list=[]; Dl=[]
    for n in range(1,K+1):
        i=w.alive_list[w.r.integers(len(w.alive_list))]; nb=list(w.nb[i])
        if nb:
            thi=0.5*np.log(w.t[i]/w.d[i]); j=random.choices(nb,weights=[np.exp(thi-0.5*np.log(w.t[m]/w.d[m])) for m in nb])[0]
            m=kt[j]>kt[i]; kt[i,m]=kt[j,m]; klt[i,m]=klt[j,m]; kld[i,m]=kld[j,m]
            m=kt[i]>kt[j]; kt[j,m]=kt[i,m]; klt[j,m]=klt[i,m]; kld[j,m]=kld[i,m]
            born.clear(); ti,di,tj,dj=w.t[i],w.d[i],w.t[j],w.d[j]
            if (ti-tj)*(di-dj)<=0:
                if random.random()<di/(di+dj): w.t[i],w.d[i]=ti,(di+dj)/2; w.t[j],w.d[j]=tj/2,dj/2; c=w.new(tj/2,di/2)
                else: w.t[j],w.d[j]=tj,(di+dj)/2; w.t[i],w.d[i]=ti/2,di/2; c=w.new(ti/2,dj/2)
                w.link(c,i); w.link(c,j)
            else:
                dom,sub=(i,j) if ti>tj else (j,i)
                if random.random()<w.d[dom]/(w.d[dom]+w.d[sub]):
                    w.t[dom]+=w.t[sub]; w.d[dom]+=w.d[sub]
                    for q in list(w.nb[sub]):
                        w.nb[q].discard(sub)
                        if q!=dom: w.link(dom,q)
                    w.nb[sub]=set(); w.kill(sub); uid[sub]=-1
                else:
                    tD,dD,tS,dS=w.t[dom],w.d[dom],w.t[sub],w.d[sub]
                    w.t[dom],w.d[dom],w.t[sub],w.d[sub]=tD/2,dD/2,tS/2,dS/2
                    for (a,b) in ((tD/2,dS/2),(tS/2,dD/2)):
                        c=w.new(a,b); w.link(c,dom); w.link(c,sub)
            w.e+=1
            for c in born:
                uid[c]=nuid[0]; nuid[0]+=1; pk=kt[i]>=kt[j]
                kt[c]=np.maximum(kt[i],kt[j]); klt[c]=np.where(pk,klt[i],klt[j]); kld[c]=np.where(pk,kld[i],kld[j])
            for k in (i,j):
                if w.alive[k]: own(k,float(n))
            for s in range(S):   # a source that has died is replaced by a fresh one
                if uid[src[s]]!=suid[s] or not w.alive[src[s]]: pick_source(s,float(n))
        if n>=burn and n%every==0:
            lt=np.log(w.t); ld=np.log(w.d); nodes=list(w.alive_list)
            thr_list.append(float(np.median([abs(lt[a]-lt[b])+abs(ld[a]-ld[b]) for a in nodes[:6000] for b in w.nb[a] if a<b])))
            balls=np.zeros(10)
            for s in range(S):
                slot=src[s]; dist={slot:0}; dq=deque([slot])
                while dq:
                    u=dq.popleft()
                    for v in w.nb[u]:
                        if v not in dist: dist[v]=dist[u]+1; dq.append(v)
                dd=np.array(list(dist.values()))
                for r in range(10): balls[r]+=np.sum(dd<=r)
                for a,r in dist.items():
                    if 1<=r<=6:
                        know.setdefault(r,[]).append(kt[a,s]>=0)
                        if kt[a,s]>=0: samples.setdefault(r,[]).append(abs(klt[a,s]-lt[slot])+abs(kld[a,s]-ld[slot]))
            Dl.append([np.log(balls[r+1]/balls[r])/np.log((r+1)/r) for r in range(1,6)])
    thr=float(np.mean(thr_list)); med={r:float(np.median(v)) for r,v in samples.items() if len(v)>=40}
    pts=[(0,0.0)]+sorted(med.items()); rstar=None
    for (r0,e0),(r1,e1) in zip(pts,pts[1:]):
        if e1>=thr: rstar=r0+(thr-e0)/(e1-e0)*(r1-r0); break
    D=np.mean(np.array(Dl),axis=0)
    Dstar=None
    if rstar is not None:
        # local dimension is defined between integer radii r->r+1 (r>=1); interpolate at r*
        x=np.arange(1,6)+0.5
        Dstar=float(np.interp(rstar,x,D))
    return dict(N=len(w.alive_list),thr=thr,med=med,cover={r:float(np.mean(v)) for r,v in know.items()},rstar=rstar,D=D.tolist(),Dstar=Dstar)
if __name__=="__main__":
    seed=int(sys.argv[1]); Nw=int(sys.argv[2]); K=int(sys.argv[3])
    res=run(seed,Nw,K)
    if res is None: print(f"seed {seed}: collapsed"); sys.exit()
    json.dump(res,open(f"h3_{seed}_{Nw}.json","w"))
    e=" ".join(f"r{r}:{res['med'][r]:.2f}({res['cover'][r]:.0%})" for r in sorted(res['med']))
    rs=f"{res['rstar']:.2f}" if res['rstar'] is not None else "beyond"
    ds=f"{res['Dstar']:.2f}" if res['Dstar'] is not None else "n/a"
    print(f"seed {seed} from {Nw} -> {res['N']} parts: threshold {res['thr']:.2f} | error(coverage) {e} | horizon {rs} steps | dimension at horizon {ds} | local dim r1..5 {np.round(res['D'],2).tolist()}",flush=True)
