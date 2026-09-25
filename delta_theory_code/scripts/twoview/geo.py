import numpy as np, random
from collections import deque
from tv import World
def bfs(w,src):
    dist={src:0}; dq=deque([src])
    while dq:
        u=dq.popleft()
        for v in w.nb[u]:
            if v not in dist: dist[v]=dist[u]+1; dq.append(v)
    return dist
for seed in (1,2):
    w=World(200,seed,rule='twoview'); marks=[1000,3000,10000,30000]
    while marks:
        idx=np.flatnonzero(w.alive)
        if len(idx)>=marks[0]:
            marks.pop(0); rng=random.Random(seed); srcs=rng.sample(list(idx),12)
            means=[]; ecc=[]; balls=np.zeros(40)
            for s0 in srcs:
                d=np.array(list(bfs(w,s0).values())); means.append(d.mean()); ecc.append(d.max())
                for r in range(40): balls[r]+=np.sum(d<=r)
            balls/=len(srcs)
            growth=" ".join(f"{int(balls[r])}" for r in range(1,9))
            print(f"s{seed} N={len(idx):6d}: mean distance={np.mean(means):.2f}, farthest={np.mean(ecc):.1f}, parts within r=1..8: {growth}",flush=True)
        w.step()
