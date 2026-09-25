import os as _os_root
_ROOT=_os_root.path.dirname(_os_root.path.dirname(_os_root.path.abspath(__file__)))
import os
import numpy as np, random, sys
sys.path.insert(0,os.path.join(_ROOT,'binding'))
import bind
from bind import World
# Polarity test. A part's polarity is the sign of its rapidity relative to the whole (more continuity than
# difference, or more difference than continuity). A pair's antisymmetric cross term tau_a delta_b - tau_b delta_a
# = 2 I eta_a eta_b sinh(theta_a - theta_b) is "same magnitude, opposite sign" between the two views.
# Questions: (1) do bound pairs of opposite polarity stay together more than bound pairs of the same polarity?
# (2) is polarity locked inside bound structures?  Run with silent absorption (Part II) and with vanishing as an act.
from vworld import V
def margin(w,a,b):
    sg=w.sig.get(w.key(a,b),0.0)
    if sg>=0: return 0.0
    ea,eb=np.sqrt(w.t[a]*w.d[a]),np.sqrt(w.t[b]*w.d[b]); dth=0.5*np.log(w.t[a]/w.d[a])-0.5*np.log(w.t[b]/w.d[b])
    kin=4*ea*eb*np.sinh(dth/2)**2
    return np.inf if kin==0 else (-sg)*(w.t[a]+w.t[b])/kin
def th(w,k):
    # rapidity relative to the whole, using the parts' own totals (relations may hold some difference)
    if not hasattr(w,'_tot') or w._tot[0]!=w.e:
        al=w.al; w._tot=(w.e,w.t[al].sum(),w.d[al].sum())
    return 0.5*np.log((w.t[k]/w._tot[1])/(w.d[k]/w._tot[2]))
def run(seed,mode,N0=2500,K=8000):
    random.seed(seed); w=V(seed,mode)
    while 2<=len(w.al)<N0: w.step()
    if len(w.al)<N0: return None
    pairs=[]
    for a in list(w.al):
        for b in w.nb[a]:
            if a<b and margin(w,a,b)>1: pairs.append((a,b,np.sign(th(w,a))*np.sign(th(w,b)),np.sign(th(w,a)-th(w,b))))
    sign0={k:np.sign(th(w,k)) for k in w.al}; members={x for p in pairs for x in p[:2]}
    for _ in range(K): w.step()
    out={}
    for cls,name in ((-1,'opposite'),(1,'same')):
        P=[p for p in pairs if p[2]==cls]; n=len(P)
        if n==0: continue
        bound=merged=0; kept=0
        for a,b,_,s0 in P:
            if w.alive[a] and w.alive[b]:
                if b in w.nb[a] and margin(w,a,b)>1:
                    bound+=1; kept+= np.sign(th(w,a)-th(w,b))==s0
            elif w.alive[a] or w.alive[b]: merged+=1      # one of them was taken in (the pair came together)
        out[name]=(n,bound/n,merged/n,kept/max(bound,1))
    alive=[k for k in sign0 if w.alive[k]]
    lock_b=np.mean([np.sign(th(w,k))==sign0[k] for k in alive if k in members])
    lock_u=np.mean([np.sign(th(w,k))==sign0[k] for k in alive if k not in members])
    return out,lock_b,lock_u,len(pairs),len(w.al)
if __name__=="__main__":
    mode=sys.argv[1]
    for seed in [int(x) for x in sys.argv[2].split(",")]:
        r=run(seed,mode)
        if r is None: print(f"[{mode} s{seed}] collapsed"); continue
        out,lb,lu,npairs,N=r
        s=" | ".join(f"{k}: {v[0]} pairs, still bound {v[1]:.0%}, merged {v[2]:.0%}, sign kept {v[3]:.0%}" for k,v in out.items())
        print(f"[{mode} s{seed}] {npairs} bound pairs at 2,500 parts -> after 8,000 events: {s} || polarity kept: bound members {lb:.0%}, others {lu:.0%}",flush=True)
