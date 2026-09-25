import os as _os_root
_ROOT=_os_root.path.dirname(_os_root.path.dirname(_os_root.path.abspath(__file__)))
import os
import numpy as np, random, sys, json
from collections import deque
sys.path.insert(0,os.path.join(_ROOT,'space'))
from space import World
seed=int(sys.argv[1]); N_WARM=int(sys.argv[2]); K=int(sys.argv[3]); S=int(sys.argv[4])
w=World(seed,'pair',cap=60000)
while 2<=len(w.alive_list)<N_WARM: w.step()
if len(w.alive_list)<N_WARM: print("universe collapsed; try another seed"); sys.exit()
cap=len(w.t); uid=np.full(cap,-1,dtype=np.int64); nuid=0
for k in w.alive_list: uid[k]=nuid; nuid+=1
# choose sources: every giant plus random others
nodes=list(w.alive_list); eta=np.sqrt(w.t[nodes]*w.d[nodes]); tot=eta.sum()
giants=[k for k,e in zip(nodes,eta) if e>0.01*tot]
rest=[k for k in nodes if k not in set(giants)]
src_slots=giants+list(np.random.default_rng(seed).choice(rest,S-len(giants),replace=False))
src_uid=np.array([uid[k] for k in src_slots]); src_is_giant=np.array([k in set(giants) for k in src_slots])
kt=np.full((cap,S),-1.0,dtype=np.float64); klt=np.zeros((cap,S),dtype=np.float32); kld=np.zeros((cap,S),dtype=np.float32)
def own_update(k,now):
    hit=np.flatnonzero(src_uid==uid[k])
    for s in hit: kt[k,s]=now; klt[k,s]=np.log(w.t[k]); kld[k,s]=np.log(w.d[k])
def merge(a,b):   # both keep, for every source, the fresher record (a chain of registrations, Ch. 9)
    m=kt[b]>kt[a]; kt[a,m]=kt[b,m]; klt[a,m]=klt[b,m]; kld[a,m]=kld[b,m]
    m=kt[a]>kt[b]; kt[b,m]=kt[a,m]; klt[b,m]=klt[a,m]; kld[b,m]=kld[a,m]
for k in src_slots: own_update(k,0.0)
change={'giant':[], 'other':[]}
# wrap the world's step to intercept encounters
orig_new=w.new
born=[]
def new_hook(t,d):
    k=orig_new(t,d); born.append(k); return k
w.new=new_hook
for n in range(1,K+1):
    i=w.alive_list[w.r.integers(len(w.alive_list))]; nb=list(w.nb[i])
    if not nb: continue
    thi=0.5*np.log(w.t[i]/w.d[i]); j=random.choices(nb,weights=[np.exp(thi-0.5*np.log(w.t[m]/w.d[m])) for m in nb])[0]
    merge(i,j)
    before={k:(np.log(w.t[k]),np.log(w.d[k])) for k in (i,j)}
    eta_i,eta_j=np.sqrt(w.t[i]*w.d[i]),np.sqrt(w.t[j]*w.d[j])
    born.clear()
    # replay the derived event on (i,j): reuse World.step's logic by forcing the pair
    ti,di,tj,dj=w.t[i],w.d[i],w.t[j],w.d[j]
    if (ti-tj)*(di-dj)<=0:
        if random.random()<di/(di+dj): w.t[i],w.d[i]=ti,(di+dj)/2; w.t[j],w.d[j]=tj/2,dj/2; c=w.new(tj/2,di/2)
        else: w.t[j],w.d[j]=tj,(di+dj)/2; w.t[i],w.d[i]=ti/2,di/2; c=w.new(ti/2,dj/2)
        w.link(c,i); w.link(c,j)
    else:
        dom,sub=(i,j) if ti>tj else (j,i)
        if random.random()<w.d[dom]/(w.d[dom]+w.d[sub]):
            w.t[dom]+=w.t[sub]; w.d[dom]+=w.d[sub]
            for m in list(w.nb[sub]):
                w.nb[m].discard(sub)
                if m!=dom: w.link(dom,m)
            w.nb[sub]=set(); w.kill(sub); uid[sub]=-1
        else:
            tD,dD,tS,dS=w.t[dom],w.d[dom],w.t[sub],w.d[sub]
            w.t[dom],w.d[dom],w.t[sub],w.d[sub]=tD/2,dD/2,tS/2,dS/2
            for (a,b) in ((tD/2,dS/2),(tS/2,dD/2)):
                c=w.new(a,b); w.link(c,dom); w.link(c,sub)
    w.e+=1
    for c in born:   # a newborn knows what its parents knew
        uid[c]=nuid; nuid+=1
        kt[c]=np.maximum(kt[i],kt[j]); pick=kt[i]>=kt[j]
        klt[c]=np.where(pick,klt[i],klt[j]); kld[c]=np.where(pick,kld[i],kld[j])
    for k in (i,j):
        if w.alive[k]:
            own_update(k,float(n))
            dl=abs(np.log(w.t[k])-before[k][0])+abs(np.log(w.d[k])-before[k][1])
            big=max(eta_i,eta_j)>0.01*np.sqrt(w.t[w.alive_list]*w.d[w.alive_list]).sum() if n%200==0 else None
            (change['giant'] if (np.sqrt(w.t[k]*w.d[k])>0.01) else change['other']).append(dl)
# measure: how wrong is what each part knows about each source, as a function of distance to it
nodes=list(w.alive_list); lt_now=np.log(w.t); ld_now=np.log(w.d)
edge_diff=[abs(lt_now[a]-lt_now[b])+abs(ld_now[a]-ld_now[b]) for a in nodes for b in w.nb[a] if a<b]
thr=float(np.median(edge_diff))
res={'giant':{}, 'other':{}}
for s,(slot,g) in enumerate(zip(src_slots,src_is_giant)):
    if not w.alive[slot] or uid[slot]!=src_uid[s]: continue
    dist={slot:0}; dq=deque([slot])
    while dq:
        u=dq.popleft()
        for v in w.nb[u]:
            if v not in dist: dist[v]=dist[u]+1; dq.append(v)
    for a,r in dist.items():
        if r==0 or r>8: continue
        key='giant' if g else 'other'
        know=kt[a,s]>=0
        err=abs(klt[a,s]-lt_now[slot])+abs(kld[a,s]-ld_now[slot]) if know else np.nan
        res[key].setdefault(r,[]).append(err)
out=dict(threshold=thr,N=len(nodes),K=K,res={k:{int(r):[float(x) for x in v] for r,v in d.items()} for k,d in res.items()},
         change={k:[float(x) for x in v[-20000:]] for k,v in change.items()})
json.dump(out,open(f"hz_{seed}.json","w"))
print(f"seed {seed}: N={len(nodes)} after {K} encounters; neighbour difference (threshold) = {thr:.3f}")
for key in ('giant','other'):
    row=[]
    for r in sorted(res[key]):
        v=np.array(res[key][r]); known=~np.isnan(v)
        med=np.median(v[known]) if known.any() else float('nan')
        row.append(f"r={r}: knows {known.mean():.0%}, error {med:.2f}")
    print(f"  sources that are {key}s: "+" | ".join(row))
for key in ('giant','other'):
    v=np.array(change[key]); print(f"  typical change per encounter for {key} parts (log units): median {np.median(v):.3f}" if len(v) else "")
