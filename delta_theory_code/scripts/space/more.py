import numpy as np, random
from space import World, bfs
# 1) how often does the first asymmetry survive?
surv=0; early=0; T=150
for seed in range(1000,1000+T):
    w=World(seed,'pair')
    while 2<=len(w.alive_list)<300: w.step()
    if len(w.alive_list)>=300: surv+=1
    elif w.e<=5: early+=1
print(f"first asymmetry: {surv}/{T} universes grew past 300 parts; {early}/{T} closed within 5 encounters")
# 2) do giants act as shortcuts? grow the surviving universe (seed 4) to 12,000 parts, then remove the heaviest parts
w=World(4,'pair')
while len(w.alive_list)<12000: w.step()
nodes=list(w.alive_list); eta={k:np.sqrt(w.t[k]*w.d[k]) for k in nodes}; tot=sum(eta.values())
rng=np.random.default_rng(7)
def mean_dist(excluded):
    ok=[k for k in nodes if k not in excluded]; ds=[]
    for s0 in [ok[q] for q in rng.choice(len(ok),20,replace=False)]:
        dist={s0:0}; dq=[s0]; h=0
        while h<len(dq):
            u=dq[h]; h+=1
            for v in w.nb[u]:
                if v not in dist and v not in excluded: dist[v]=dist[u]+1; dq.append(v)
        ds.append((np.mean(list(dist.values())),len(dist)/len(ok)))
    return np.mean([a for a,_ in ds]),np.mean([b for _,b in ds])
giants={k for k in nodes if eta[k]>0.01*tot}
deg=sorted(nodes,key=lambda k:-len(w.nb[k]))
hubs=set(deg[:len(giants)])
print(f"universe of {len(nodes)} parts: {len(giants)} giants hold {sum(eta[k] for k in giants)/tot:.0%} of eta; their mean degree {np.mean([len(w.nb[k]) for k in giants]):.1f} vs overall {np.mean([len(w.nb[k]) for k in nodes]):.2f}")
for label,ex in (("nothing removed",set()),("giants removed",giants),("same number of top hubs removed",hubs)):
    md,frac=mean_dist(ex); print(f"  {label:32s}: mean distance {md:.2f}, share of others still reachable {frac:.2f}")
