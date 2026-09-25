import numpy as np, json, sys
from edge import Universe
def run(q, seed, Ntarget=15000, Emax=400000, N0=1000):
    U=Universe(N0,seed=seed)
    while U.n<Ntarget and U.e<Emax and U.n>=2:
        U.step(q)
    eta=np.sqrt(U.t[:U.n]*U.d[:U.n]); return U, eta
def loghist(x, nb=30):
    x=x[x>0]; b=np.logspace(np.log10(x.min()),np.log10(x.max())*1.0000001,nb+1)
    h,_=np.histogram(x,bins=b); w=np.diff(b); c=np.sqrt(b[:-1]*b[1:]); dens=h/(w*len(x))
    return c,dens,h
def tailslope(x, lo_factor=2.0, mincount=5):
    c,dens,h=loghist(x)
    med=np.median(x); m=(c>lo_factor*med)&(h>=mincount)
    if m.sum()<4: return float('nan'), int(m.sum())
    p=np.polyfit(np.log10(c[m]),np.log10(dens[m]),1); return p[0], int(m.sum())
out={}
for q in (0.83,0.7,0.5,0.0):
    for seed in (7,8,9):
        U,eta=run(q,seed)
        status="collapsed" if U.n<2 else f"N={U.n} after {U.e} events"
        if U.n<100: print(f"q={q} seed={seed}: {status}"); continue
        s,npts=tailslope(eta)
        lt=np.array(U.lifetimes)
        ls,lpts=tailslope(lt.astype(float)) if len(lt)>200 else (float('nan'),0)
        span=np.log10(eta.max()/np.median(eta))
        print(f"q={q} seed={seed}: {status}; eta: max/median=10^{span:.2f}, tail slope={s:.2f} ({npts} bins); deaths={U.deaths}, lifetime tail slope={ls:.2f} ({lpts} bins)",flush=True)
        out[f"{q}_{seed}"]={"eta":eta.tolist(),"life":lt.tolist()}
json.dump(out,open("spectra.json","w"))
