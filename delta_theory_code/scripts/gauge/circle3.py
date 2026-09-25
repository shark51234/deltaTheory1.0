import numpy as np
from covariant import colour, network
import importlib.util, sys
src=open('circle.py').read().split("for seed,N in")[0]; exec(src)       # reuse roundmap/commutant without rerunning tests
# Time-dependent version of a local symmetry: a family M_0, M_1=J M_0 J^-1, M_2, ... that STAYS confined to part k.
# Find the largest space of part-k transformations that one round maps back into itself, and how a round acts on it.
def invariant_local(J,S):
    m=J.shape[0]; Ji=np.linalg.inv(J); s=len(S); inside=np.zeros((m,m),bool); inside[np.ix_(S,S)]=True
    def emb(x): M=np.zeros((m,m)); M[np.ix_(S,S)]=x.reshape(s,s); return M
    V=np.eye(s*s)                                           # start: all transformations confined to part k
    for it in range(50):
        imgs=np.array([(J@emb(v)@Ji) for v in V.T])         # one round later
        out=np.array([im[~inside] for im in imgs]).T; ins=np.array([im[inside] for im in imgs]).T
        P=V@np.linalg.pinv(V); res=np.vstack([out,(np.eye(s*s)-P)@ins])
        u,sv,vt=np.linalg.svd(res,full_matrices=True); r=int((sv>1e-7*max(sv.max(),1)).sum()); null=vt[r:].T
        if null.shape[1]==V.shape[1]: break
        V=V@null; V,_=np.linalg.qr(V)
        if V.shape[1]==0: return 0,np.array([])
    A=np.linalg.pinv(V)@np.array([(J@emb(v)@Ji)[inside] for v in V.T]).T   # how one round acts on this space
    return V.shape[1],np.linalg.eigvals(A)
for seed,N in ((3,12),(5,20)):
    edges,n=network(seed,N); col,C=colour(edges); E=len(edges); J=roundmap(edges,n,col,C)
    for k in range(n):
        S=[k,n+k]+[2*n+e for e,(u,v) in enumerate(edges) if k in (u,v)]+[2*n+E+e for e,(u,v) in enumerate(edges) if k in (u,v)]
        d,ev=invariant_local(J,S)
        print(f"seed {seed}, part {k:2d} (degree {len(S)//2-1}): transformations that stay confined to this part forever: {d}; "
              f"a round acts on them with eigenvalues {np.round(ev,3).tolist()}")
