import numpy as np
from covariant import colour, network
from circle import roundmap, commutant
np.set_printoptions(precision=3,suppress=True,linewidth=150)
for seed,N in ((3,12),(5,20),(11,16)):
    edges,n=network(seed,N); col,C=colour(edges); E=len(edges); J=roundmap(edges,n,col,C)
    names=[f"lnτ{k}" for k in range(n)]+[f"lnδ{k}" for k in range(n)]+[f"x{edges[e]}" for e in range(E)]+[f"y{edges[e]}" for e in range(E)]
    for k in range(n):
        S=[k,n+k]+[2*n+e for e,(u,v) in enumerate(edges) if k in (u,v)]+[2*n+E+e for e,(u,v) in enumerate(edges) if k in (u,v)]
        b,s=commutant(J,[S])
        for M in b:
            M=M/np.abs(M).max(); nz=np.argwhere(np.abs(M)>1e-6)
            ev=np.linalg.eigvals(M); r=np.linalg.matrix_rank(M,1e-6)
            print(f"seed {seed}: part {k} (degree {len([e for e in edges if k in e])}): rank {r}, eigenvalues nonzero {np.round(ev[np.abs(ev)>1e-6],3)}, "
                  f"M^2 size {np.abs(M@M).max():.1e}")
            rows=sorted(set(i for i,j in nz)); colsn=sorted(set(j for i,j in nz))
            print("     acts on", [names[j] for j in colsn], "-> writes into", [names[i] for i in rows])
