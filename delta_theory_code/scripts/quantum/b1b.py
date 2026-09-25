import numpy as np
from perspectival import colour, network
def evolve(tau,dl,rel,edges,col,C):
    tau=tau.copy(); dl=dl.copy(); rel=dict(rel)
    for t in range(C):
        for (u,v) in edges:
            if col[(u,v)]!=t: continue
            T=tau[u]+tau[v]; D=dl[u]+dl[v]; xu,yu=rel[(u,v)]; rel[(u,v)]=(tau[u]/T,dl[u]/D)
            tau[u],tau[v]=T*yu,T*(1-yu); dl[u],dl[v]=D*xu,D*(1-xu)
    return tau,dl,rel
def boost(tau,dl,rel,k,lam):
    # part k changes its own frame: its continuity scales by lam, its difference by 1/lam; its relations'
    # remembered splits are re-expressed in the new frame
    tau=tau.copy(); dl=dl.copy(); rel=dict(rel); tau[k]*=lam; dl[k]/=lam
    for (u,v),(x,y) in rel.items():
        if u==k: rel[(u,v)]=(lam*x/(lam*x+(1-x)), (y/lam)/((y/lam)+(1-y)))
        elif v==k: rel[(u,v)]=(x/(x+lam*(1-x)), y/(y+(1-y)/lam))
    return tau,dl,rel
edges,n=network(5,16); col,C=colour(edges); rng=np.random.default_rng(2)
tau=np.exp(0.3*rng.normal(size=n)); dl=np.exp(0.3*rng.normal(size=n))
rel={(u,v):(tau[u]/(tau[u]+tau[v]),dl[u]/(dl[u]+dl[v])) for (u,v) in edges}
tau,dl,rel=evolve(tau,dl,rel,edges,col,C)      # let records become stale first
for label,ks in (("every part at once (a global boost)",list(range(n))),("one part only (a local boost)",[3])):
    t1,d1,r1=tau,dl,rel
    for k in ks: t1,d1,r1=boost(t1,d1,r1,k,1.7)
    a=evolve(t1,d1,r1,edges,col,C)
    b=evolve(tau,dl,rel,edges,col,C)
    for k in ks: b=boost(*b,k,1.7)
    err=max(np.abs(np.log(a[0]/b[0])).max(),np.abs(np.log(a[1]/b[1])).max())
    print(f"{label}: evolve-then-boost vs boost-then-evolve differ by {err:.2e} (in log units)")
