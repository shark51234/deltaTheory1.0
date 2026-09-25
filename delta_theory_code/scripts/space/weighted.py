import numpy as np, heapq, json
from space import World
def snapshot(w):
    nodes=list(w.alive_list); idx={k:n for n,k in enumerate(nodes)}
    lt=np.log(w.t[nodes]); ld=np.log(w.d[nodes])
    adj=[[idx[m] for m in w.nb[k]] for k in nodes]
    eta=np.sqrt(w.t[nodes]*w.d[nodes])
    return dict(lt=lt,ld=ld,adj=adj,eta=eta)
def lengths(S,metric):
    lt,ld=S['lt'],S['ld']
    def L(a,b):
        x=abs(lt[a]-lt[b]); y=abs(ld[a]-ld[b])
        return 1.0 if metric=='steps' else (np.hypot(x,y) if metric=='L2' else x+y)
    return L
def dijkstra(S,src,L):
    dist={src:0.0}; pq=[(0.0,src)]
    while pq:
        d0,u=heapq.heappop(pq)
        if d0>dist[u]: continue
        for v in S['adj'][u]:
            nd=d0+L(u,v)
            if nd<dist.get(v,1e300): dist[v]=nd; heapq.heappush(pq,(nd,v))
    return np.array(list(dist.values()))
w=World(4,'pair'); snaps={}
for target in (4000,12000,25000):
    while len(w.alive_list)<target: w.step()
    snaps[target]=snapshot(w)
rng=np.random.default_rng(11); out={}
for metric in ('steps','L2','L1'):
    print(f"--- distance measured as {metric} ---")
    for N,S in snaps.items():
        L=lengths(S,metric); n=len(S['adj'])
        srcs=rng.choice(n,16,replace=False); alld=[dijkstra(S,int(s),L) for s in srcs]
        mean=np.mean([d.mean() for d in alld])
        # 'dimension seen by a processor of reach rho': d ln(parts within rho) / d ln rho
        q=np.quantile(np.concatenate(alld),[0.002,0.01,0.05,0.2,0.5])
        rhos=q[q>0]
        vols=[np.mean([np.sum(d<=r) for d in alld]) for r in rhos]
        dims=[np.log(vols[k+1]/vols[k])/np.log(rhos[k+1]/rhos[k]) for k in range(len(rhos)-1)]
        print(f"N={N:6d}: mean distance {mean:8.3f} | parts within reach at the 0.2/1/5/20/50% distance quantiles: {np.round(vols).astype(int).tolist()} | dimension seen at increasing reach: {np.round(dims,2).tolist()}",flush=True)
        out[f"{metric}_{N}"]=dict(mean=float(mean),vols=[float(v) for v in vols],rhos=[float(r) for r in rhos],dims=[float(x) for x in dims])
json.dump(out,open("weighted.json","w"))
