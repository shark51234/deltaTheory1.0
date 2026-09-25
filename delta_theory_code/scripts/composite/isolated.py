import os as _os_root
_ROOT=_os_root.path.dirname(_os_root.path.dirname(_os_root.path.abspath(__file__)))
import os
import numpy as np
import sys
from layer import *
# check the reduced layer against the full linearised share-swap (eigenvalues must be a subset)
sys.path.insert(0,os.path.join(_ROOT,'gauge')); exec(open(os.path.join(_ROOT,'gauge')+'/circle.py').read().split("for seed,N in")[0])
n,edges,cols=cluster("net",12,seed=3); col={e:c for e,c in zip(edges,cols)}; C=max(cols)+1
full=np.linalg.eigvals(roundmap(edges,n,col,C)); red=np.linalg.eigvals(round_matrix(n,edges,cols))
print("reduced rapidity layer reproduces the full layer's eigenvalues:", all(np.abs(full-l).min()<1e-6 for l in red))
# A single isolated composite: its internal circles
def circles(J):
    ev,V=np.linalg.eig(J); rot=ev[ev.imag>1e-9]; ang=np.sort(np.angle(rot))
    degen=sum(1 for i in range(len(ang)-1) if abs(ang[i+1]-ang[i])<1e-6)
    return ang,degen
for kind,N in (("pair",2),("triangle",3),("ring",6),("ring",8),("ring",12),("net",12)):
    n,edges,cols=cluster(kind,N); J=round_matrix(n,edges,cols); ang,degen=circles(J)
    print(f"{kind:8s} ({n:2d} parts): all eigenvalues on the unit circle {np.allclose(np.abs(np.linalg.eigvals(J)),1)}; "
          f"rotating modes {len(ang)} (turns per round: {np.round(ang/(2*np.pi),3).tolist()}); degenerate pairs {degen}")
# the pair's circle, exactly: rotate (d, r) by any angle, keep the pair's total rapidity
n,edges,cols=cluster("pair",2); J=round_matrix(n,edges,cols)
for a in (0.3,1.0,2.2):
    c,s=np.cos(a),np.sin(a)
    # coordinates (th0, th1, r): d = th0 - th1, P = th0 + th1
    T=np.array([[1,1,0],[1,-1,0],[0,0,1.]]); R=np.array([[1,0,0],[0,c,-s],[0,s,c]]); Rt=np.linalg.inv(T)@R@T
    print(f"pair: rotating its internal state by {a}: commutes with its contact to {np.abs(J@Rt-Rt@J).max():.0e}")
