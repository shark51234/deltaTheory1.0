import os as _os_root
_ROOT=_os_root.path.dirname(_os_root.path.dirname(_os_root.path.abspath(__file__)))
import os
import numpy as np, sys
sys.path.insert(0,os.path.join(_ROOT,'quantum'))
from perspectival import colour, network
# Rapidity sector of the lossless layer. Linearising the share-swap around even shares, sizes decouple exactly
# and each contact on relation e=(u,v) does:  theta_u, theta_v -> mean -/+ r_e/2 ;  r_e -> theta_u - theta_v
# (r_e = the relative rapidity the relation remembers from its last contact).
def contact(m,n,i,u,v):
    K=np.eye(m); ri=n+i; K[[u,v,ri],:]=0
    K[u,u]=K[u,v]=K[v,u]=K[v,v]=0.5; K[u,ri]=-0.5; K[v,ri]=0.5; K[ri,u]=1; K[ri,v]=-1
    return K
def round_matrix(n,edges,cols):
    m=n+len(edges); J=np.eye(m)
    for t in sorted(set(cols)):
        for i,(u,v) in enumerate(edges):
            if cols[i]==t: J=contact(m,n,i,u,v)@J
    return J
def cluster(kind,N,seed=5):
    if kind=="pair": return 2,[(0,1)],[0]
    if kind=="triangle": return 3,[(0,1),(1,2),(0,2)],[0,1,2]
    if kind=="ring": return N,[(k,(k+1)%N) for k in range(N)],[k%2 for k in range(N)]
    edges,n=network(seed,N); col,C=colour(edges); return n,edges,[col[e] for e in edges]
