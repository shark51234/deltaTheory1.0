import os as _os_root
_ROOT=_os_root.path.dirname(_os_root.path.dirname(_os_root.path.abspath(__file__)))
import os
import numpy as np, sys
sys.path.insert(0,os.path.join(_ROOT,'quantum'))
from perspectival import colour, network
# Frame-carrying exchange. Each part's state (tau, delta) is written in its OWN frame, an arbitrary label.
# Each relation e=(u,v) carries a link a_e: the rapidity that carries v's frame into u's frame.
# The remembered split (u's share of continuity and of difference at last contact) is a ratio: frame-free.
def evolve(tau,dl,rec,link,edges,col,C,rounds=1):
    tau=tau.copy(); dl=dl.copy(); rec=dict(rec)
    for _ in range(rounds):
        for t in range(C):
            for e in edges:
                if col[e]!=t: continue
                u,v=e; g=np.exp(link[e])
                tv,dv=tau[v]*g,dl[v]/g                      # v's state carried into u's frame
                T=tau[u]+tv; D=dl[u]+dv; xu,yu=rec[e]; rec[e]=(tau[u]/T,dl[u]/D)
                tau[u],dl[u]=T*yu,D*xu                      # the share-swap, computed in u's frame
                tau[v],dl[v]=T*(1-yu)/g,D*(1-xu)*g          # v's new state carried back into its own frame
    return tau,dl,rec
def relabel(tau,dl,link,c):
    # part k re-labels its own frame by rapidity c[k]; each relation's link absorbs the change
    return tau*np.exp(c),dl*np.exp(-c),{(u,v):a+c[u]-c[v] for (u,v),a in link.items()}
def gap(A,B):
    (t1,d1,r1),(t2,d2,r2)=A,B
    return max(np.abs(np.log(t1/t2)).max(),np.abs(np.log(d1/d2)).max(),
               max(max(abs(r1[e][0]-r2[e][0]),abs(r1[e][1]-r2[e][1])) for e in r1))
def setup(seed,N,spread=0.2,fluxsize=0.1):
    edges,n=network(seed,N); col,C=colour(edges); rng=np.random.default_rng(seed)
    tau=np.exp(spread*rng.normal(size=n)); dl=np.exp(spread*rng.normal(size=n))
    link={e:fluxsize*rng.normal() for e in edges}
    rec={e:(0.5+0.05*rng.normal(),0.5+0.05*rng.normal()) for e in edges}
    return edges,n,col,C,tau,dl,link,rec,rng
if __name__=="__main__":
    print("TEST 1: does re-labelling frames commute with the dynamics?")
    for seed,N in ((3,12),(5,20),(8,40)):
        edges,n,col,C,tau,dl,link,rec,rng=setup(seed,N)
        for label,c in (("one part",np.eye(n)[n//2]*0.8),("every part, independently",rng.normal(0,0.8,n))):
            for R in (1,200):
                A=evolve(tau,dl,rec,link,edges,col,C,R); tA,dA,_=relabel(A[0],A[1],link,c)
                tg,dg,lg=relabel(tau,dl,link,c); B=evolve(tg,dg,rec,lg,edges,col,C,R)
                print(f"  {n:2d} parts, {label:26s}, {R:3d} rounds: difference {gap((tA,dA,A[2]),B):.1e}")
    print("\nTEST 3 (flat case): links with zero sum around every loop, against the old rule with no links")
    for seed,N in ((3,12),(5,20),(8,40)):
        edges,n,col,C,tau,dl,link,rec,rng=setup(seed,N)
        zero={e:0.0 for e in edges}; c=rng.normal(0,1.0,n)
        old=evolve(tau,dl,rec,zero,edges,col,C,500)                 # the rule as it was
        tg,dg,flat=relabel(tau,dl,zero,c)                          # a flat configuration: every loop sums to zero
        new=evolve(tg,dg,rec,flat,edges,col,C,500)
        back=relabel(new[0],new[1],flat,-c)
        print(f"  {n:2d} parts, 500 rounds: new rule in a flat configuration vs old rule: difference {gap((back[0],back[1],new[2]),old):.1e}")
