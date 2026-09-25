import numpy as np, sys
from edge import Universe
N0=1000; E=60000
for q in (0.83,0.84,0.845,0.85,0.855):
    for seed in (7,8):
        U=Universe(N0,seed=seed); traj=[]; maxshare=[]
        for e in range(E):
            if e%6000==0:
                eta=np.sqrt(U.t[:U.n]*U.d[:U.n]); traj.append(U.n); maxshare.append(round(float(eta.max()/eta.sum()),3))
            if U.n<2 or U.n>150000: break
            U.step(q)
        print(f"q={q:.3f} seed={seed}: N={traj} end={U.n} at e={U.e}; largest part's share of sum(eta)={maxshare}", flush=True)
