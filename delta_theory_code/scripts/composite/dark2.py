import numpy as np
from layer import *
from coupled import build
from circle_local import local_commutant
# Whatever a commuting transformation confined to A (plus the joining relation) produces: can B EVER notice it?
for kind,N in (("triangle",3),("ring",8),("ring",12),("net",12)):
    n,E,JT,JA,iA,iB,pa,m=build(kind,N,pick=0)
    basis=local_commutant(JT,iA+[m-1]); rng=np.random.default_rng(3); worstB=0; size=0
    for B in basis:
        for _ in range(3):
            y=B@rng.normal(size=m); size=max(size,np.abs(y).max()); z=y.copy()
            for t in range(3000):
                worstB=max(worstB,np.abs(z[iB]).max()); z=JT@z
    print(f"joined {kind}s of {n}: {len(basis)} commuting local transformations; largest thing they produce {size:.1e}; "
          f"largest trace of it ever seen in B over 3000 rounds {worstB:.1e}")
