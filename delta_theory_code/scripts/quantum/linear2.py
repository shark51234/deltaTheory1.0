import numpy as np
from linear import round_map
def colour(edges):
    col={}
    for e in edges:
        used={col[f] for f in col if set(f)&set(e)}; c=0
        while c in used: c+=1
        col[e]=c
    return col,max(col.values())+1
def jac(edges,n,tau0,dl0,eps=1e-7):
    col,C=colour(edges); keys=[(u,v) for (u,v) in edges]+[(v,u) for (u,v) in edges]
    rec0={(u,v):dl0[v] for (u,v) in keys}
    def vec(s): return np.concatenate([s[0],s[1],[s[2][k] for k in keys]])
    def unvec(x): return (x[:n].copy(),x[n:2*n].copy(),{k:x[2*n+i] for i,k in enumerate(keys)})
    # linearize around a fixed point? A non-uniform background is not stationary, so linearize the round map
    # around the background's own trajectory for one round and study the product over many rounds instead
    return col,C,keys,vec,unvec
def growth(edges,n,tau0,dl0,rounds=(10,100,1000),eps=1e-6,trials=6,seed=0):
    col,C,keys,vec,unvec=jac(edges,n,tau0,dl0)
    rng=np.random.default_rng(seed)
    base=(tau0.copy(),dl0.copy(),{k:dl0[k[1]] for k in keys})
    out=[]
    for k in rounds:
        ratios=[]
        for _ in range(trials):
            d=rng.normal(size=2*n)*eps
            pert=(tau0*(1+d[:n]),dl0*(1+d[n:]),{kk:dl0[kk[1]]*(1+d[n+kk[1]]) for kk in keys})
            a=base; b=pert
            for _ in range(k): a=round_map(a,edges,col,C,n); b=round_map(b,edges,col,C,n)
            diff=np.concatenate([np.log(b[0]/a[0]),np.log(b[1]/a[1])])
            ratios.append(np.linalg.norm(diff)/np.linalg.norm(d))
        out.append((k,np.mean(ratios),np.max(ratios)))
    return out
rng=np.random.default_rng(3)
# a random tree-like relational network (children attach to both ends of a random relation, as in the rules)
edges=[(0,1)]; n=2
for _ in range(18):
    u,v=edges[rng.integers(len(edges))]; c=n; n+=1; edges+= [(u,c),(v,c)]
for label,(t0,d0) in (("uniform background",(np.ones(n),np.ones(n))),
                      ("random sizes and rapidities",(np.exp(rng.normal(0,0.7,n)),np.exp(rng.normal(0,0.7,n))))):
    g=growth(edges,n,t0,d0)
    print(f"random 20-part network, {label}: how much a small disturbance grows after k rounds: "+"; ".join(f"k={k}: mean x{m:.2f}, max x{M:.2f}" for k,m,M in g))
