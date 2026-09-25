import numpy as np, sys, json
from collections import defaultdict
from bind import World
seed=int(sys.argv[1]); N0=int(sys.argv[2]); K=int(sys.argv[3]); EVERY=int(sys.argv[4])
w=World(seed,records=True)
while 2<=len(w.al)<N0: w.step()
if len(w.al)<N0: print("collapsed"); sys.exit()
uid=np.full(len(w.t),-1,dtype=np.int64); nu=[0]
for k in w.al: uid[k]=nu[0]; nu[0]+=1
orig=w.new
def hook(t,d):
    k=orig(t,d); uid[k]=nu[0]; nu[0]+=1; return k
w.new=hook
def bonds():
    out={}
    for (a,b),sg in w.sig.items():
        if sg>=0 or not (w.alive[a] and w.alive[b]) or b not in w.nb[a]: continue
        ea,eb=np.sqrt(w.t[a]*w.d[a]),np.sqrt(w.t[b]*w.d[b]); dth=0.5*np.log(w.t[a]/w.d[a])-0.5*np.log(w.t[b]/w.d[b])
        if (-sg)*(w.t[a]+w.t[b])>4*ea*eb*np.sinh(dth/2)**2:
            moving=abs(dth)>abs(np.log(ea/eb))          # differ more in motion than in size (spacelike pair)
            out[(min(uid[a],uid[b]),max(uid[a],uid[b]))]=moving
    return out
def components(edges):
    adj=defaultdict(set)
    for a,b in edges: adj[a].add(b); adj[b].add(a)
    seen=set(); comps=[]
    for v in adj:
        if v in seen: continue
        st=[v]; seen.add(v); c={v}
        while st:
            u=st.pop()
            for x in adj[u]:
                if x not in seen: seen.add(x); st.append(x); c.add(x)
        comps.append(frozenset(c))
    return comps
snaps=[]
for n in range(K+1):
    if n%EVERY==0:
        B=bonds(); alive={int(uid[k]) for k in w.al}
        snaps.append(dict(B=B,alive=alive,all=components(B.keys()),mov=components([k for k,m in B.items() if m])))
    if len(w.al)<2: break
    w.step()
# 1) bond lifetimes by type (runs of consecutive snapshots; type at first sighting; censored runs excluded)
life=defaultdict(list); first={}; runs={}
for s,S in enumerate(snaps):
    for k in list(runs):
        if k not in S['B']: life[first.pop(k)].append(s-runs.pop(k))
    for k,m in S['B'].items():
        if k not in runs: runs[k]=s; first[k]=m
print(f"seed {seed}: {len(snaps)} snapshots every {EVERY} encounters; universe {len(w.al)} parts at the end")
for m,label in ((True,'moving bonds (differ more in motion)'),(False,'size-dominated bonds')):
    v=np.array(life[m])*EVERY
    if len(v): print(f"  {label:38s}: {len(v)} ended; median life {np.median(v):.0f}, mean {v.mean():.0f}, lasting 5+ snapshots {np.mean(v>=5*EVERY):.1%}")
share=np.mean([np.mean(list(S['B'].values())) for S in snaps if S['B']])
print(f"  share of bonds that are moving: {share:.1%}")
# 2) structures: size, and how long their members stay together (and how much the membership turns over)
def follow(kind,lag):
    ret=[]; turn=[]; memb=[]; n=0
    for s in range(len(snaps)-lag):
        later=snaps[s+lag][kind]
        for C in snaps[s][kind]:
            if len(C)<3: continue
            n+=1; best=max(later,key=lambda D: len(C&D),default=frozenset())
            ov=len(C&best); ret.append(ov/len(C)); turn.append(1-ov/len(best) if best else 1.0)
            memb.append(len(C&snaps[s+lag]['alive'])/len(C))
    return n,np.mean(ret),np.mean(turn),np.mean(memb)
for kind,label in (('mov','structures held by moving bonds'),('all','structures held by any bonds')):
    sizes=[len(C) for S in snaps for C in S[kind]]
    print(f"  {label}: {np.mean([len(S[kind]) for S in snaps]):.0f} per snapshot, mean size {np.mean(sizes):.1f}, largest {max(sizes)}")
    for lag in (1,3,6):
        n,r,t,m=follow(kind,lag)
        print(f"    after {lag*EVERY:6d} encounters: members still together {r:5.1%} | members still alive {m:5.1%} | new members in the matched structure {t:5.1%}  (n={n})")
