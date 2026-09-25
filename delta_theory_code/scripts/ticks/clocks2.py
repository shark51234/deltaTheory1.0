import os as _os_root
_ROOT=_os_root.path.dirname(_os_root.path.dirname(_os_root.path.abspath(__file__)))
import os
import numpy as np, sys
sys.path.insert(0,os.path.join(_ROOT,'activity')); sys.path.insert(0,'.')
from clocks import Clocked
# desynchronisation R = 1 - sum(eta) over the life of more universes; and how many clocks stop (absorbed parts)
for seed in (4,5,6,7):
    w=Clocked(200,seed,'clock_delta'); Rs=[]
    for e in range(400001):
        if e%100000==0:
            idx=np.flatnonzero(w.alive); Rs.append((len(idx),1-np.sqrt(w.t[idx]*w.d[idx]).sum()))
        if w.alive.sum()<2 or len(w.free)<500: break
        w.step()
    print(f"seed {seed}: " + "  ".join(f"N={n} R={r:.4f}" for n,r in Rs) + f"  | births {w.c['births']} deaths(stopped clocks) {w.c['deaths']}",flush=True)
