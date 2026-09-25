import numpy as np
from perspectival import colour, network
def rounds(state,edges,col,C,k):
    tau,dl,rel=state
    for _ in range(k):
        for t in range(C):
            for (u,v) in edges:
                if col[(u,v)]!=t: continue
                T=tau[u]+tau[v]; D=dl[u]+dl[v]
                xu,yu=rel[(u,v)]                   # the split the relation registered at the pair's last contact
                rel[(u,v)]=(tau[u]/T,dl[u]/D)      # register the current split
                tau[u],tau[v]=T*yu,T*(1-yu)        # execute the swap of the registered split on the current totals
                dl[u],dl[v]=D*xu,D*(1-xu)
    return tau,dl,rel
def start(spread,seed):
    edges,n=network(seed); col,C=colour(edges); rng=np.random.default_rng(seed+1)
    tau=np.exp(rng.normal(0,spread,n)); dl=np.exp(rng.normal(0,spread,n))
    rel={(u,v):(tau[u]/(tau[u]+tau[v]),dl[u]/(dl[u]+dl[v])) for (u,v) in edges}
    return edges,n,col,C,(tau,dl,rel)
print("delayed share-swap (the relation remembers the pair's split; the swap of that split is executed on current totals)")
for spread in (0.05,0.2,0.4,1.0,2.0):
    edges,n,col,C,s=start(spread,3); T0,D0=s[0].sum(),s[1].sum()
    tau,dl,rel=rounds((s[0].copy(),s[1].copy(),dict(s[2])),edges,col,C,5000)
    th=0.5*np.log(tau/dl); eta=np.sqrt(tau*dl)
    # disturbance growth around this uneven state
    base=(tau.copy(),dl.copy(),dict(rel)); rng=np.random.default_rng(7); g=[]
    for k in (10,100,1000):
        rs=[]
        for _ in range(4):
            d=1e-7*rng.normal(size=2*n)
            a=(base[0].copy(),base[1].copy(),dict(base[2])); b=(base[0]*(1+d[:n]),base[1]*(1+d[n:]),dict(base[2]))
            a=rounds(a,edges,col,C,k); b=rounds(b,edges,col,C,k)
            rs.append(np.linalg.norm(np.concatenate([np.log(b[0]/a[0]),np.log(b[1]/a[1])]))/np.linalg.norm(d))
        g.append(f"k={k}: x{np.mean(rs):.2f}")
    print(f"  spread {spread:4.2f}: 5000 rounds valid={bool((tau>0).all() and (dl>0).all())}; totals drift {abs(tau.sum()-T0):.1e},{abs(dl.sum()-D0):.1e}; "
          f"rapidity spread {th.std():.3f}; size spread {np.log(eta).std():.3f} | disturbance growth {', '.join(g)}")
