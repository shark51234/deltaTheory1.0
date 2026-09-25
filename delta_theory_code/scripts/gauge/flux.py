import numpy as np
from covariant import evolve, relabel, colour, network
# What does a link configuration with nonzero loop sums (flux) do?  Start every part identical and at rest
# in its own frame, records even, and give the links either a flat pattern (control) or a flux pattern.
def triangles(edges,n):
    idx={e:i for i,e in enumerate(edges)}; tri=[]
    for c in range(2,n):
        u,v=[e for e in edges if e[1]==c][0][0],[e for e in edges if e[1]==c][1][0]
        a,b=sorted((u,v)); tri.append(((a,b),(a,c),(b,c)))
    return tri
def invariants(tau,dl,link,edges):
    th=0.5*np.log(tau/dl); eta=np.sqrt(tau*dl)
    d={e:th[e[0]]-th[e[1]]-link[e] for e in edges}          # relative rapidity across each relation, frame-free
    return eta,d
def run(seed,N,size,flat,rounds=3000):
    edges,n=network(seed,N); col,C=colour(edges); rng=np.random.default_rng(seed+7)
    tau=np.ones(n); dl=np.ones(n); rec={e:(0.5,0.5) for e in edges}
    if flat: c=rng.normal(0,size,n); link={(u,v):c[u]-c[v] for (u,v) in edges}
    else: link={e:size*rng.normal() for e in edges}
    tri=triangles(edges,n); Phi=[L1-L3+L2 for L1,L2,L3 in [(link[a],link[b2],link[b]) for a,b,b2 in [(t[0],t[1],t[2]) for t in tri]]]
    out=[]
    for r in range(0,rounds,10):
        tau,dl,rec=evolve(tau,dl,rec,link,edges,col,C,10)
        if not (np.isfinite(tau).all() and (tau>0).all() and (dl>0).all()): return out,r,None
        eta,d=invariants(tau,dl,link,edges)
        loops=[d[a]+d[b2]-d[b] for a,b,b2 in tri]           # around u->v->c->u
        out.append((r+10,np.log(eta).mean(),np.log(eta).std(),np.sqrt(np.mean([x*x for x in d.values()])),
                    max(abs(L+P) for L,P in zip(loops,Phi))))
    return out,rounds,np.array(Phi)
for seed,N in ((3,12),(5,20)):
    for size in (0.003,0.01,0.03):
        for flat in (True,False):
            out,r,Phi=run(seed,N,size,flat)
            tag="flat (control)" if flat else "flux          "
            if Phi is None or not out: print(f"{N} parts, links ~{size}, {tag}: BLEW UP at round {r}"); continue
            a=out[0]; b=out[len(out)//2]; z=out[-1]
            print(f"{N} parts, links ~{size}, {tag}: mean ln(size) {a[1]:+.1e} -> {b[1]:+.1e} -> {z[1]:+.1e} (rounds {a[0]},{b[0]},{z[0]}); "
                  f"size spread {z[2]:.1e}; rms relative rapidity {a[3]:.1e} -> {z[3]:.1e}; loop sums vs -flux: worst {max(o[4] for o in out):.0e}")
