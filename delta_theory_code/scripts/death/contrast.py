import numpy as np, sys
sys.argv=['x']
from causal import World
for seed in (1,2):
    w=World(200,seed,'oneway'); w.inertia=True; w.reldeath=False; w.spread=False
    for e in range(60001):
        if e in (10000,30000,60000):
            idx=np.flatnonzero(w.alive); eta=np.sqrt(w.t[idx]*w.d[idx]); pos={k:n for n,k in enumerate(idx)}
            lc=[]
            for n,k in enumerate(idx):
                ns=[pos[m] for m in w.nb[k] if m in pos]
                if ns and eta[n]>0: lc.append(np.log10(eta[n]/np.median(eta[ns])))
            lc=np.array(lc); q=np.percentile(lc,[10,25,50,75,90])
            tot=eta.sum(); small=eta[eta<0.01*tot]
            print(f"s{seed} e{e}: N={len(idx)}, local contrast log10 percentiles 10/25/50/75/90 = {np.round(q,2)}, non-giant parts hold {small.sum()/tot:.3f} of eta",flush=True)
        if w.alive.sum()<2: print("collapsed"); break
        w.step()
