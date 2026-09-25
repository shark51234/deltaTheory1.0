import numpy as np
from layer import *
from coupled import build
from circle_local import local_commutant
# Are the local rotations found for rings and nets just rotations of "dark" waves -- internal waves with a node at the
# joining member, which the other composite can never see?  Split A's waves into dark and bright and look at what the
# commuting transformations do to the bright ones.
for kind,N in (("triangle",3),("ring",8),("ring",16),("net",12),("net",24)):
    n,E,JT,JA,iA,iB,pa,m=build(kind,N,pick=0)
    ev,V=np.linalg.eig(JA); amp=np.abs(V[pa,:])/np.linalg.norm(V,axis=0)
    dark=[j for j in range(len(ev)) if amp[j]<1e-9 and abs(ev[j].imag)>1e-9]
    bright=[j for j in range(len(ev)) if amp[j]>=1e-9]
    basis=local_commutant(JT,iA+[m-1])
    Vb=np.zeros((m,len(bright)),complex); Vb[iA,:]=V[:,bright]
    worst=0; rot_on_bright=0; rng=np.random.default_rng(2)
    for _ in range(300):
        if not basis: break
        M=sum(rng.normal()*B for B in basis)
        act=M@Vb                                   # what the transformation does to the bright waves
        # express the result in A's wave basis and keep only its bright components
        c=np.linalg.solve(V,act[iA,:]); cb=c[bright,:]
        worst=max(worst,np.abs(cb-np.diag(np.diag(cb))*0).max())
        ev_b=np.linalg.eigvals(cb) if cb.size else np.array([0])
        rot_on_bright+=np.abs(np.angle(ev_b[np.abs(ev_b)>1e-8])).max(initial=0)>1e-6
    print(f"joined {kind}s of {n}: dark internal waves {len(dark)//1} (of {int((np.abs(ev.imag)>1e-9).sum())}); "
          f"commuting local transformations {len(basis)}; largest effect on bright waves {worst:.1e}; rotating them: {rot_on_bright} of 300")
