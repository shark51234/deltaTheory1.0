import numpy as np, random, sys
class World:
    def __init__(s,N0,seed,cap=70000,rule='twoview',q=1.0):
        s.r=np.random.default_rng(seed); random.seed(seed); s.rule=rule; s.q=q
        s.t=np.zeros(cap); s.d=np.zeros(cap); s.alive=np.zeros(cap,bool)
        s.nb=[set() for _ in range(cap)]; s.free=list(range(cap-1,-1,-1)); s.e=0; s.deaths=0
        t=s.r.uniform(.2,1.8,N0); d=s.r.uniform(.2,1.8,N0); t/=t.sum(); d/=d.sum()
        ks=[s.new(a,b) for a,b in zip(t,d)]
        for x in range(N0): s.link(ks[x],ks[(x+1)%N0])
    def new(s,t,d):
        k=s.free.pop(); s.t[k]=t; s.d[k]=d; s.alive[k]=True; s.nb[k]=set(); return k
    def link(s,a,b):
        if a!=b: s.nb[a].add(b); s.nb[b].add(a)
    def remove(s,k,heir):
        for m in list(s.nb[k]):
            s.nb[m].discard(k)
            if m!=heir: s.link(heir,m)
        s.nb[k]=set(); s.alive[k]=False; s.free.append(k)
    def step(s):
        idx=np.flatnonzero(s.alive); pt=s.t[idx]
        i=int(idx[np.searchsorted(np.cumsum(pt),s.r.random()*pt.sum())])
        nb=list(s.nb[i]); j=random.choices(nb,weights=[s.d[k] for k in nb])[0]
        ti,di,tj,dj=s.t[i],s.d[i],s.t[j],s.d[j]
        if s.rule=='twoview':
            if random.random()<di/(di+dj):   # i's self acts (keeps its row); for j the relation acts (its registration of i is born)
                s.t[i],s.d[i]=ti,(di+dj)/2; s.t[j],s.d[j]=tj/2,dj/2; c=s.new(tj/2,di/2)
            else:                            # mirror
                s.t[j],s.d[j]=tj,(di+dj)/2; s.t[i],s.d[i]=ti/2,di/2; c=s.new(ti/2,dj/2)
            s.link(c,i); s.link(c,j)
        elif s.rule=='row':                  # previous test: initiator's row decides; self absorbs w.p. q
            if random.random()<di/(di+dj):
                if random.random()<s.q:
                    s.t[i]+=tj; s.d[i]+=dj; s.remove(j,heir=i); s.deaths+=1
            else:
                s.t[i],s.d[i],s.t[j],s.d[j]=ti/2,di/2,tj/2,dj/2
                for (a,b) in ((ti/2,dj/2),(tj/2,di/2)):
                    c=s.new(a,b); s.link(c,i); s.link(c,j)
        s.e+=1
    def stats(s):
        idx=np.flatnonzero(s.alive); t=s.t[idx]; d=s.d[idx]; eta=np.sqrt(t*d)
        med=np.median(eta); rel=eta/med
        # tail slope of the log-binned density above 2x median
        b=np.logspace(np.log10(rel.min()),np.log10(rel.max())*1.000001,31); h,_=np.histogram(rel,bins=b)
        c=np.sqrt(b[:-1]*b[1:]); dens=h/(np.diff(b)*len(rel)); m=(c>2)&(h>=5)
        slope=np.polyfit(np.log10(c[m]),np.log10(dens[m]),1)[0] if m.sum()>=4 else float('nan')
        # local contrast: log of each part's eta over the median eta of its neighbours
        pos={k:n for n,k in enumerate(idx)}
        lc=[]
        for n,k in enumerate(idx[:5000]):
            ns=[pos[m] for m in s.nb[k] if m in pos]
            if ns: lc.append(np.log10(eta[n]/np.median(eta[ns])))
        lc=np.array(lc); iqr=np.percentile(lc,75)-np.percentile(lc,25)
        theta=0.5*np.log((t/t.sum())/(d/d.sum()))
        deg=np.array([len(s.nb[k]) for k in idx])
        return dict(N=len(idx),R=float(1-eta.sum()),span=float(np.log10(rel.max())),slope=float(slope),
                    local_iqr=float(iqr),theta_sd=float(theta.std()),giant=float(eta.max()/eta.sum()),
                    deg_mean=float(deg.mean()),deg_max=int(deg.max()))
if __name__=="__main__":
    rule=sys.argv[1]; seed=int(sys.argv[2]); marks=[int(x) for x in sys.argv[3].split(',')]; q=float(sys.argv[4]) if len(sys.argv)>4 else 1.0
    w=World(200,seed,rule=rule,q=q); mk=list(marks)
    while mk:
        if len(np.flatnonzero(w.alive))>=mk[0]:
            st=w.stats(); mk.pop(0)
            print(f"[{rule} s{seed}] N={st['N']:6d} events={w.e:6d} R={st['R']:.3f} span=10^{st['span']:.2f} tail={st['slope']:.2f} local_iqr={st['local_iqr']:.3f} theta_sd={st['theta_sd']:.3f} giant={st['giant']:.4f} deg_mean={st['deg_mean']:.2f} deg_max={st['deg_max']}",flush=True)
        w.step()
