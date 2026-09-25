import numpy as np, sys, random
from collections import defaultdict
from bind import World
seed=int(sys.argv[1]); N0=int(sys.argv[2]); K=int(sys.argv[3])
w=World(seed,records=True)
while 2<=len(w.al)<N0: w.step()
if len(w.al)<N0: print("collapsed"); sys.exit()
def state(a,b):
    """binding margin: debt*(tau_a+tau_b) / kinetic surplus; bound iff margin > 1"""
    sg=w.sig.get(w.key(a,b),0.0)
    if sg>=0: return 0.0
    ea,eb=np.sqrt(w.t[a]*w.d[a]),np.sqrt(w.t[b]*w.d[b]); dth=0.5*np.log(w.t[a]/w.d[a])-0.5*np.log(w.t[b]/w.d[b])
    kin=4*ea*eb*np.sinh(dth/2)**2
    return np.inf if kin==0 else (-sg)*(w.t[a]+w.t[b])/kin
# bookkeeping on bonds, keyed by slot pair (slots are stable while both parts are alive)
bound={}
def refresh(parts):
    for a in parts:
        if not w.alive[a]: continue
        for b in w.nb[a]:
            k=w.key(a,b); m=state(a,b)
            if m>1 and k not in bound: bound[k]=dict(t0=w.e)
            elif m<=1 and k in bound: bound.pop(k)
refresh(list(w.al))
stats=defaultdict(lambda:[0,0])   # kind -> [survived, total]
by_excl=defaultdict(lambda:[0,0]); by_margin=defaultdict(lambda:[0,0]); deepen=[0,0]
for n in range(K):
    i=w.al[w.r.integers(len(w.al))]; nb=list(w.nb[i])
    if not nb: w.e+=1; continue
    thi=0.5*np.log(w.t[i]/w.d[i]); j=random.choices(nb,weights=[np.exp(thi-0.5*np.log(w.t[m]/w.d[m])) for m in nb])[0]
    # bonds that involve i or j, as they are before the encounter
    before=[]
    for x in (i,j):
        for y in list(w.nb[x]):
            k=w.key(x,y)
            if k in bound:
                own=(k==w.key(i,j)); deg=min(len(w.nb[x]),len(w.nb[y])); marg=state(x,y)
                before.append((k,own,deg,marg,w.sig.get(k,0.0)))
    # replay the event exactly as World.step would, by forcing the chosen pair
    rs=w.r; st=w.r.integers
    class Fixed:
        def integers(self,n): return w.pos[i]
        def __getattr__(self,a): return getattr(rs,a)
    w.r=Fixed(); _choices=random.choices; random.choices=lambda pop,weights=None,k=1: [j]
    ti,di,tj,dj=w.t[i],w.d[i],w.t[j],w.d[j]; spacelike=(ti-tj)*(di-dj)<=0
    nal=len(w.al); w.step(); w.r=rs; random.choices=_choices
    kind_base='spacelike' if spacelike else ('timelike-absorb' if len(w.al)<nal else 'timelike-cross')
    refresh([i,j]+[k for k in w.al[-2:]])
    seen=set()
    for (k,own,deg,marg,sg0) in before:
        if k in seen: continue
        seen.add(k); a,b=k
        alive=w.alive[a] and w.alive[b] and b in w.nb[a]
        ok = alive and state(a,b)>1
        kind=('bond partners meet' if own else 'a member meets someone else')+' / '+kind_base
        stats[kind][0]+=ok; stats[kind][1]+=1
        if not own:
            ex='exclusive (member has <=3 relations)' if deg<=3 else ('4-6 relations' if deg<=6 else '7+ relations')
            by_excl[ex][0]+=ok; by_excl[ex][1]+=1
        mb='margin <2' if marg<2 else ('2-10' if marg<10 else '10+')
        by_margin[mb][0]+=ok; by_margin[mb][1]+=1
        if own and alive:
            deepen[0]+= w.sig.get(k,0.0)<sg0; deepen[1]+=1
print(f"seed {seed}: bonds tracked through {K} encounters (universe {len(w.al)} parts at the end)")
print("  survival of a bond through one encounter of its members:")
for kind,(s,t) in sorted(stats.items()): print(f"    {kind:52s} survived {s/t:5.1%}  (n={t})")
print("  when a member meets someone else, by how many relations the members have:")
for kind,(s,t) in sorted(by_excl.items()): print(f"    {kind:40s} survived {s/t:5.1%}  (n={t})")
print("  by binding margin before the encounter (debt x continuity over kinetic surplus):")
for kind,(s,t) in sorted(by_margin.items()): print(f"    {kind:12s} survived {s/t:5.1%}  (n={t})")
print(f"  when bond partners meet each other, the debt deepened in {deepen[0]/max(deepen[1],1):.0%} of cases")
