import numpy as np
from perspectival import colour
M=10; edges=[(k,(k+1)%M) for k in range(M)]; col,C=colour(edges); unit=np.log(2)
def trial(seed,maxr=20000,noise=1e-3,src=0):
    rng=np.random.default_rng(seed)
    tau=np.exp(noise*rng.normal(size=M)); dl=np.exp(noise*rng.normal(size=M))
    tau[src]*=np.sqrt(2); dl[src]/=np.sqrt(2)
    rel={(u,v):(tau[u]/(tau[u]+tau[v]),dl[u]/(dl[u]+dl[v])) for (u,v) in edges}
    T0,D0=tau.sum(),dl.sum(); dens=np.zeros(M)
    for r in range(maxr):
        for t in range(C):
            for (u,v) in edges:
                if col[(u,v)]!=t: continue
                T=tau[u]+tau[v]; D=dl[u]+dl[v]; xu,yu=rel[(u,v)]; rel[(u,v)]=(tau[u]/T,dl[u]/D)
                tau[u],tau[v]=T*yu,T*(1-yu); dl[u],dl[v]=D*xu,D*(1-xu)
        lt=np.log(tau/(T0/M)); ld=np.log(dl/(D0/M)); dev=np.abs(lt)+np.abs(ld); dens+=lt**2+ld**2
        if r>=10 and dev.max()>=unit: return int(dev.argmax()),r,dens/dens.sum()
    return None,maxr,dens/dens.sum()
outs=[]; shares=[]; times=[]
for s in range(300):
    k,r,sh=trial(s)
    if k is not None: outs.append(k); times.append(r)
    shares.append(sh)
outs=np.array(outs); freq=np.bincount(outs,minlength=M)/len(outs); share=np.mean(shares,axis=0)
print(f"{len(outs)} of 300 trials produced an event (a full halving concentrated at one member); median wait {np.median(times):.0f} rounds")
print("member:                    ",list(range(M)))
print("share of events:           ",np.round(freq,3).tolist())
print("squared-amplitude share:   ",np.round(share,3).tolist())
chi=np.sum((freq-share)**2/share)*len(outs)
print(f"correlation between event frequency and squared-amplitude share: {np.corrcoef(freq,share)[0,1]:.3f}; chi-square {chi:.1f} on {M-1} degrees of freedom")
