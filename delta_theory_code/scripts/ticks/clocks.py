import os as _os_root
_ROOT=_os_root.path.dirname(_os_root.path.dirname(_os_root.path.abspath(__file__)))
import os
import numpy as np, random, sys
sys.path.insert(0,os.path.join(_ROOT,'activity'))
from derived import World
# The note read on the Part II universe (derived activity rule, 'clock_delta'):
#   a tick of part i = an event that changes its eta (birth, two-view, absorption); exchanges are not ticks
#   the clock reading of i, counted from the whole, is sum of its eta-steps = 1 - eta_i  (telescoping)
#   remainder Delta_i = eta_i when its clock stops; sum over parts of Delta = 1 - R  (R = motion = desynchronisation)
class Clocked(World):
    def __init__(s,*a,**k):
        super().__init__(*a,**k); s.last=np.zeros(s.cap,dtype=np.int64); s.nt=np.zeros(s.cap,dtype=np.int64)
    def event(s,i,j):
        s.last[i]=s.e; s.last[j]=s.e; s.nt[i]+=1; s.nt[j]+=1
        super().event(i,j)
    def new(s,t,d):
        k=super().new(t,d); 
        if hasattr(s,'last'): s.last[k]=s.e; s.nt[k]=0
        return k
def measure(w):
    idx=np.flatnonzero(w.alive); t,d=w.t[idx],w.d[idx]; eta=np.sqrt(t*d); th=0.5*np.log(t/d)
    N=len(idx); idle=w.e-w.last[idx]
    stopped=idle>20*N/1.0          # no tick for 20 population-times: effectively a stopped clock
    # desynchronisation of each part from its neighbours
    pos={k:n for n,k in enumerate(idx)}; dsync=np.zeros(N)
    for n,k in enumerate(idx):
        ns=[pos[m] for m in w.nb[k] if m in pos]
        dsync[n]=np.abs(th[n]-np.average(th[ns],weights=eta[ns])) if ns else np.nan
    return dict(N=N,R=1-eta.sum(),frac_stopped=stopped.mean(),
                sync_stopped=np.nanmedian(dsync[stopped]) if stopped.any() else np.nan,
                sync_active=np.nanmedian(dsync[~stopped]),share_stopped=eta[stopped].sum(),
                rms_theta=np.sqrt(np.average(th**2,weights=eta)))
if __name__=="__main__":
  for seed in (1,2,3):
      w=Clocked(200,seed,'clock_delta'); out=[]
      for e in range(400001):
          if e%50000==0:
              m=measure(w); out.append(m)
              print(f"seed {seed} e{e:6d}: parts {m['N']:6d}  R(desync) {m['R']:.4f}  rms rapidity {m['rms_theta']:.3f}  "
                    f"stopped clocks {m['frac_stopped']:.2f} holding {m['share_stopped']:.3f} of the whole  "
                    f"desync of stopped/active {m['sync_stopped']:.3f}/{m['sync_active']:.3f}",flush=True)
          if w.alive.sum()<2 or len(w.free)<500: print("  stop:",'collapse' if w.alive.sum()<2 else 'cap',e); break
          w.step()
