import numpy as np, sys
from collections import deque
sys.path.insert(0,'.')
from vanish import Vanishing
# Does vanishing-as-an-act change "space"? Compare the relation network of the old rule (absorb) and the new
# rule (vanish) at the same size: ball growth (dimension seen at reach r), and what happens without the giants.
def grow(seed,mode,N):
    w=Vanishing(200,seed,'clock_delta',mode=mode)
    while w.alive.sum()<N and len(w.free)>500: w.step()
    return w
def balls(w,nodes,src,block=set(),R=8):
    out=[]
    for s in src:
        dist={s:0}; q=deque([s]); cnt=np.zeros(R+1)
        while q:
            u=q.popleft(); d=dist[u]
            if d>=R: continue
            for v in w.nb[u]:
                if v not in dist and v not in block: dist[v]=d+1; q.append(v)
        for d in dist.values(): cnt[d]+=1
        out.append(np.cumsum(cnt))
    return np.array(out),dist
for mode in ('absorb','vanish'):
    for seed in (1,2):
        w=grow(seed,mode,30000); nodes=np.flatnonzero(w.alive); eta=np.sqrt(w.t[nodes]*w.d[nodes]); tot=eta.sum()
        giants=set(nodes[eta>0.01*tot].tolist()); rng=np.random.default_rng(seed)
        src=[int(x) for x in rng.choice([k for k in nodes if k not in giants],40,replace=False)]
        B,_=balls(w,nodes,src); m=B.mean(0)
        D=[np.log(m[r+1]/m[r])/np.log((r+1)/r) for r in range(1,6)]
        # reach without the giants: how much of the universe a typical part can still get to
        Bg,_=balls(w,nodes,src[:10],block=giants,R=60); frac=np.mean([b[-1] for b in Bg])/len(nodes)
        deg=np.mean([len(w.nb[k]) for k in nodes])
        print(f"{mode:6s} seed {seed}: N={len(nodes)} giants {len(giants)} (largest {eta.max()/tot:.3f}) mean degree {deg:.1f} | "
              f"ball growth dimension at r=1..5: {np.round(D,1).tolist()} | reachable without giants {frac:.1%}",flush=True)
