import numpy as np
from perspectival import colour
M=10; edges=[(k,(k+1)%M) for k in range(M)]; col,C=colour(edges)
def run(src,R=40000,seed=0,noise=1e-3):
    rng=np.random.default_rng(seed)
    tau=np.exp(noise*rng.normal(size=M)); dl=np.exp(noise*rng.normal(size=M))
    tau[src]*=np.sqrt(2); dl[src]/=np.sqrt(2)
    rel={(u,v):(tau[u]/(tau[u]+tau[v]),dl[u]/(dl[u]+dl[v])) for (u,v) in edges}
    T0,D0=tau.sum(),dl.sum(); LT=np.zeros((R,M)); LD=np.zeros((R,M)); X=np.zeros((R,M)); Y=np.zeros((R,M))
    for r in range(R):
        for t in range(C):
            for (u,v) in edges:
                if col[(u,v)]!=t: continue
                T=tau[u]+tau[v]; D=dl[u]+dl[v]; xu,yu=rel[(u,v)]; rel[(u,v)]=(tau[u]/T,dl[u]/D)
                tau[u],tau[v]=T*yu,T*(1-yu); dl[u],dl[v]=D*xu,D*(1-xu)
        LT[r]=np.log(tau/(T0/M)); LD[r]=np.log(dl/(D0/M))
        for i,e in enumerate(edges): X[r,i],Y[r,i]=rel[e]
    # the quantum is the rotating part: fluctuations about each member's (and relation's) own average state;
    # the non-rotating part (the lambda = 1 mode) is a lasting change of the structure's shape, not the quantum
    lt=LT-LT.mean(0); ld=LD-LD.mean(0); x=X-X.mean(0); y=Y-Y.mean(0)
    th=0.5*(lt-ld)
    exc=(np.exp(-th)-1).mean(0)                       # extra registration of each member by a detector at rest with it
    dens=(lt**2+ld**2).mean(0)
    w=8*(x**2+y**2).mean(0)
    for i,(u,v) in enumerate(edges): dens[u]+=w[i]/2; dens[v]+=w[i]/2
    return exc,(th**2).mean(0),dens
for src in (0,3):
    exc,th2,q=run(src)
    pe=exc/exc.sum(); pt=th2/th2.sum(); pq=q/q.sum()
    rng=np.random.default_rng(1); N=5000
    f=np.bincount(rng.choice(M,size=N,p=pe),minlength=M)/N   # Postulate 8: the whole quantum is registered at one place
    chi=N*np.sum((f-pq)**2/pq)
    print(f"quantum placed at member {src}: all extra registrations non-negative: {bool((exc>=0).all())}")
    print("  outcome frequencies (5,000)    :",np.round(f,3).tolist())
    print("  share of the conserved total   :",np.round(pq,3).tolist())
    print("  share of squared rapidity      :",np.round(pt,3).tolist())
    print(f"  chi-square of outcomes against the conserved total: {chi:.1f} on 9 d.f.; against squared rapidity: {N*np.sum((f-pt)**2/pt):.1f}")
