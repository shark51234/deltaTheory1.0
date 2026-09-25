import numpy as np, sys, json
from collections import defaultdict
from bind import World
seed=int(sys.argv[1]); N0=int(sys.argv[2]); K=int(sys.argv[3]); EVERY=int(sys.argv[4])
w=World(seed,records=True)
while 2<=len(w.al)<N0: w.step()
if len(w.al)<N0: print("collapsed"); sys.exit()
# unique ids so that relations can be followed across slot reuse
uid=np.full(len(w.t),-1,dtype=np.int64); nu=[0]
for k in w.al: uid[k]=nu[0]; nu[0]+=1
orig_new=w.new
def new_hook(t,d):
    k=orig_new(t,d); uid[k]=nu[0]; nu[0]+=1; return k
w.new=new_hook
def snapshot():
    eta=lambda k: np.sqrt(w.t[k]*w.d[k])
    bound=set(); rows=[]
    for (a,b),sg in w.sig.items():
        if not (w.alive[a] and w.alive[b]) or b not in w.nb[a]: continue
        T=w.t[a]+w.t[b]; D=w.d[a]+w.d[b]+sg; ec=np.sqrt(T*D) if D>0 else 0.0; free=eta(a)+eta(b)
        L=abs(np.log(w.t[a]/w.t[b]))+abs(np.log(w.d[a]/w.d[b]))
        mass=abs(np.log(eta(a)/eta(b))); motion=abs(0.5*np.log(w.t[a]/w.d[a])-0.5*np.log(w.t[b]/w.d[b]))
        B=(free-ec)/free; rows.append((L,B,mass,motion))
        if ec<free: bound.add((min(uid[a],uid[b]),max(uid[a],uid[b])))
    # all relations (including those with no state) for the bound-fraction baseline by length
    allL=[]
    for a in w.al:
        for b in w.nb[a]:
            if a<b and (w.key(a,b) not in w.sig): allL.append(abs(np.log(w.t[a]/w.t[b]))+abs(np.log(w.d[a]/w.d[b])))
    return bound,rows,allL
hist=[]; rows_all=[]; allL_all=[]
for n in range(K+1):
    if n%EVERY==0:
        bnd,rows,allL=snapshot(); hist.append(bnd)
        if n>=K-5*EVERY: rows_all+=rows; allL_all+=allL
    if len(w.al)<2: break
    w.step()
# bond lifetimes: runs of consecutive snapshots in which a relation is bound (runs still open at the end are censored)
life=[]; open_runs={}
for t,bset in enumerate(hist):
    for k in list(open_runs):
        if k not in bset: life.append(t-open_runs.pop(k))
    for k in bset:
        if k not in open_runs: open_runs[k]=t
censored=[len(hist)-t0 for t0 in open_runs.values()]
# bound structures at the end: connected components of the bound relations
final=hist[-1]; adj=defaultdict(set)
for a,b in final: adj[a].add(b); adj[b].add(a)
seen=set(); comps=[]
for v in adj:
    if v in seen: continue
    stack=[v]; seen.add(v); size=0
    while stack:
        u=stack.pop(); size+=1
        for x in adj[u]:
            if x not in seen: seen.add(x); stack.append(x)
    comps.append(size)
comps=np.array(sorted(comps,reverse=True)); N=len(w.al)
print(f"seed {seed}: {N} parts at the end; {len(final)} bound relations")
print(f"  bound structures: {len(comps)}; parts in them {comps.sum()} ({comps.sum()/N:.1%}); sizes: largest {comps[:5].tolist()}, "
      f"share of size 2 = {np.mean(comps==2):.0%}, 3-5 = {np.mean((comps>=3)&(comps<=5)):.0%}, 6+ = {np.mean(comps>=6):.0%}")
life=np.array(life)*EVERY; cens=np.array(censored)*EVERY
print(f"  bond lifetimes (ended bonds, encounters): median {np.median(life):.0f}, 90th pct {np.percentile(life,90):.0f}; bonds still intact at the end: {len(cens)} (median age {np.median(cens):.0f})")
R=np.array(rows_all); A=np.array(allL_all)
edges=np.quantile(np.concatenate([R[:,0],A]),[0,0.2,0.4,0.6,0.8,1.0])
print("  binding versus the relation's length (how different the two parts are):")
for lo,hi in zip(edges[:-1],edges[1:]):
    m=(R[:,0]>=lo)&(R[:,0]<=hi); a=(A>=lo)&(A<=hi)
    nrel=m.sum()+a.sum(); nb=(R[m,1]>0).sum()
    medB=np.median(R[m,1][R[m,1]>0]) if nb>0 else 0.0
    print(f"    length {lo:5.2f}-{hi:5.2f}: bound {nb/max(nrel,1):5.1%} of relations, median binding when bound {medB:5.1%}")
b=R[R[:,1]>0]; u=R[R[:,1]<=0]
print(f"  bound pairs: median size angle {np.median(b[:,2]):.2f}, motion angle {np.median(b[:,3]):.2f}; unbound pairs with states: {np.median(u[:,2]):.2f}, {np.median(u[:,3]):.2f}")
