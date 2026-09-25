import numpy as np
from perspectival import colour
# A nearly even structure: a ring of 10 identical members, internal encounters are exchanges (the lossless layer).
M=10; edges=[(k,(k+1)%M) for k in range(M)]; col,C=colour(edges)
tau=np.ones(M); dl=np.ones(M)
tau[0]*=np.sqrt(2); dl[0]/=np.sqrt(2)            # one halving's worth of difference at member 0: |d ln tau|+|d ln delta| = ln 2
rel={(u,v):(tau[u]/(tau[u]+tau[v]),dl[u]/(dl[u]+dl[v])) for (u,v) in edges}
T0,D0=tau.sum(),dl.sum(); unit=np.log(2)
maxdev=[]; where=[]; dens=np.zeros(M); R=20000
for r in range(R):
    for t in range(C):
        for (u,v) in edges:
            if col[(u,v)]!=t: continue
            T=tau[u]+tau[v]; D=dl[u]+dl[v]; xu,yu=rel[(u,v)]; rel[(u,v)]=(tau[u]/T,dl[u]/D)
            tau[u],tau[v]=T*yu,T*(1-yu); dl[u],dl[v]=D*xu,D*(1-xu)
    lt=np.log(tau/(T0/M)); ld=np.log(dl/(D0/M))       # each member's deviation from the even state
    dev=np.abs(lt)+np.abs(ld); maxdev.append(dev.max()); where.append(int(dev.argmax()))
    dens+=lt**2+ld**2
maxdev=np.array(maxdev); where=np.array(where)
print(f"initial deviation at member 0: {unit:.3f} (one halving)")
print(f"largest deviation any member reaches after the first 10 rounds: {maxdev[10:].max():.3f} ({maxdev[10:].max()/unit:.0%} of a halving)")
print(f"rounds in which some member again carries a full halving: {np.sum(maxdev[10:]>=unit*0.999)} of {R-10}")
print(f"typical largest deviation: median {np.median(maxdev[10:]):.3f} ({np.median(maxdev[10:])/unit:.0%} of a halving)")
share=dens/dens.sum()
print("time-averaged share of the squared deviation at each member:",np.round(share,3).tolist())
