import numpy as np
from perspectival import colour, network
from conserved import round_fn
def jac(edges,n):
    col,C=colour(edges); E=len(edges); m=2*n+2*E; z0=np.zeros(m); f0=round_fn(z0,edges,col,C,n); J=np.zeros((m,m))
    for i in range(m):
        z=z0.copy(); z[i]=1e-7; J[:,i]=(round_fn(z,edges,col,C,n)-f0)/1e-7
    return J
def rot(n,E,angles_parts,angles_rel):
    m=2*n+2*E; R=np.zeros((m,m))
    for k in range(n):
        a=angles_parts[k]; c,s=np.cos(a),np.sin(a)
        R[k,k]=c; R[k,n+k]=-s; R[n+k,k]=s; R[n+k,n+k]=c          # rotate (ln tau_k, ln delta_k)
    for e in range(E):
        a=angles_rel[e]; c,s=np.cos(a),np.sin(a); i,j=2*n+e,2*n+E+e
        R[i,i]=c; R[i,j]=-s; R[j,i]=s; R[j,j]=c                    # rotate the relation's remembered split (x, y)
    return R
for seed,N in ((3,12),(5,20)):
    edges,n=network(seed,N); E=len(edges); J=jac(edges,n)
    # global rotation of every part's continuity-difference plane and every relation's memory plane
    for a in (np.pi/2,np.pi/3,0.37):
        R=rot(n,E,[a]*n,[a]*E); err=np.linalg.norm(J@R-R@J)/np.linalg.norm(J)
        print(f"{n} parts: global rotation by {a:.3f}: J R - R J relative size {err:.2e}")
    # a local rotation of one part (try its relations' memories rotated by 0, a/2, a)
    k=1; inc=[e for e,(u,v) in enumerate(edges) if k in (u,v)]
    for frac in (0,0.5,1.0):
        ap=[0.0]*n; ap[k]=0.37; ar=[0.0]*E
        for e in inc: ar[e]=0.37*frac
        R=rot(n,E,ap,ar); err=np.linalg.norm(J@R-R@J)/np.linalg.norm(J)
        print(f"   local rotation of part {k} (its relations' memories rotated by {frac} of it): relative size {err:.2e}")
