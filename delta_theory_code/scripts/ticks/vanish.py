import os as _os_root
_ROOT=_os_root.path.dirname(_os_root.path.dirname(_os_root.path.abspath(__file__)))
import os
import numpy as np, random, sys
sys.path.insert(0,os.path.join(_ROOT,'activity'))
from derived import World
# Vanishing as an act (the author's clarification): when a part's clock stops it leaves its remainder to OTHER
# parts, and the act itself disturbs the field. Continuity is what stays (Ch. 25): it stays with the part that
# registered the vanishing (the containing partner). Difference is what moves (Ch. 8): it spreads to every
# neighbour of the vanished part, in proportion to the rate at which each registers it, the Doppler factor
# e^(theta_j - theta_i) derived for the activity rule. Every recipient's eta changes: the vanishing ticks their clocks.
class Vanishing(World):
    def __init__(s,*a,mode='vanish',**k):
        super().__init__(*a,**k); s.mode=mode; s.kick=[]
    def absorb(s,keep,gone):
        if s.mode=='absorb': return super().absorb(keep,gone)
        nbrs=list(s.nb[gone]); thg=0.5*np.log(s.t[gone]/s.d[gone])
        th=np.array([0.5*np.log(s.t[m]/s.d[m]) for m in nbrs])
        w=np.exp(th-thg); w/=w.sum()
        before=th.copy()
        s.t[keep]+=s.t[gone]
        for m,wm in zip(nbrs,w): s.d[m]+=s.d[gone]*wm
        after=np.array([0.5*np.log(s.t[m]/s.d[m]) for m in nbrs])
        s.kick.append(np.abs(after-before)[[k for k,m in enumerate(nbrs) if m!=keep]].mean() if len(nbrs)>1 else 0.0)
        for m in nbrs:
            s.unlink(gone,m)
            if m!=keep: s.link(keep,m)
        s.alive[gone]=False; s.free.append(gone); s.c['deaths']+=1
def run(seed,mode,E=400000):
    w=Vanishing(200,seed,'clock_delta',mode=mode); rows=[]
    for e in range(E+1):
        if e%100000==0:
            idx=np.flatnonzero(w.alive); eta=np.sqrt(w.t[idx]*w.d[idx]); tot=eta.sum()
            rows.append((e,len(idx),1-tot,eta.max()/tot,int((eta>0.01*tot).sum())))
        if w.alive.sum()<2: rows.append(('collapse',e)); break
        if len(w.free)<500: rows.append(('cap',e)); break
        w.step()
    return rows,w
if __name__=="__main__":
    mode=sys.argv[1]
    for seed in [int(x) for x in sys.argv[2].split(',')]:
        rows,w=run(seed,mode)
        print(f"[{mode} s{seed}] births {w.c['births']} vanishings {w.c['deaths']}"+
              (f" mean kick to other neighbours {np.mean(w.kick):.3f}" if w.kick else ""),flush=True)
        for r in rows: print("    ",r if isinstance(r[0],str) else f"e{r[0]}: N={r[1]} R={r[2]:.4f} largest={r[3]:.3f} parts>1%={r[4]}",flush=True)
