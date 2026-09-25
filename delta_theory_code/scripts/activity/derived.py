import numpy as np, random, sys
class World:
    def __init__(s,N0,seed,variant,cap=60000):
        s.r=np.random.default_rng(seed); random.seed(seed); s.v=variant; s.cap=cap
        s.t=np.zeros(cap); s.d=np.zeros(cap); s.alive=np.zeros(cap,bool); s.born=np.zeros(cap,dtype=np.int64)
        s.nb=[set() for _ in range(cap)]; s.free=list(range(cap-1,-1,-1)); s.e=0
        s.ea=np.zeros(8*cap,dtype=np.int64); s.eb=np.zeros(8*cap,dtype=np.int64); s.ne=0; s.eidx={}
        s.c=dict(space=0,time=0,births=0,deaths=0)
        t=s.r.uniform(.2,1.8,N0); d=s.r.uniform(.2,1.8,N0); t/=t.sum(); d/=d.sum()
        ks=[s.new(a,b) for a,b in zip(t,d)]
        for x in range(N0): s.link(ks[x],ks[(x+1)%N0])
    def new(s,t,d):
        k=s.free.pop(); s.t[k]=t; s.d[k]=d; s.alive[k]=True; s.nb[k]=set(); s.born[k]=s.e; return k
    def link(s,a,b):
        if a==b or b in s.nb[a]: return
        s.nb[a].add(b); s.nb[b].add(a); key=(min(a,b),max(a,b))
        s.ea[s.ne]=key[0]; s.eb[s.ne]=key[1]; s.eidx[key]=s.ne; s.ne+=1
    def unlink(s,a,b):
        s.nb[a].discard(b); s.nb[b].discard(a); key=(min(a,b),max(a,b))
        k=s.eidx.pop(key); last=s.ne-1
        if k!=last:
            s.ea[k]=s.ea[last]; s.eb[k]=s.eb[last]; s.eidx[(s.ea[k],s.eb[k])]=k
        s.ne-=1
    def absorb(s,keep,gone):
        s.t[keep]+=s.t[gone]; s.d[keep]+=s.d[gone]
        for m in list(s.nb[gone]):
            s.unlink(gone,m)
            if m!=keep: s.link(keep,m)
        s.alive[gone]=False; s.free.append(gone); s.c['deaths']+=1
    def crossover(s,i,j):
        ti,di,tj,dj=s.t[i],s.d[i],s.t[j],s.d[j]
        s.t[i],s.d[i],s.t[j],s.d[j]=ti/2,di/2,tj/2,dj/2
        for (a,b) in ((ti/2,dj/2),(tj/2,di/2)):
            c=s.new(a,b); s.link(c,i); s.link(c,j)
        s.c['births']+=2
    def twoview(s,i,j):
        ti,di,tj,dj=s.t[i],s.d[i],s.t[j],s.d[j]
        if random.random()<di/(di+dj):
            s.t[i],s.d[i]=ti,(di+dj)/2; s.t[j],s.d[j]=tj/2,dj/2; c=s.new(tj/2,di/2)
        else:
            s.t[j],s.d[j]=tj,(di+dj)/2; s.t[i],s.d[i]=ti/2,di/2; c=s.new(ti/2,dj/2)
        s.link(c,i); s.link(c,j); s.c['births']+=1
    def step(s):
        if s.v.startswith('clock'):
            # one process, one clock: every part ticks at the same proper rate (optionally dilated by 1/cosh theta as seen by the whole);
            # at each tick it meets a neighbour in proportion to the rate that neighbour's ticks reach it, cosh(theta_i - theta_j)
            idx=np.flatnonzero(s.alive)
            if s.v=='clock_dilated':
                th_i=0.5*np.log(s.t[idx]/s.d[idx]); p=1/np.cosh(th_i); i=int(idx[np.searchsorted(np.cumsum(p),s.r.random()*p.sum())])
            else:
                i=int(idx[s.r.integers(len(idx))])
            nb=list(s.nb[i])
            if not nb: s.e+=1; return
            thi=0.5*np.log(s.t[i]/s.d[i])
            if s.v=='clock_delta':   # registration arrives only as propagating difference (Ch. 8): Doppler factor e^(theta_i - theta_j)
                wts=[np.exp(thi-0.5*np.log(s.t[m]/s.d[m])) for m in nb]
            else:
                wts=[np.cosh(thi-0.5*np.log(s.t[m]/s.d[m])) for m in nb]
            j=random.choices(nb,weights=wts)[0]
            s.event(i,j); return
        a=s.ea[:s.ne]; b=s.eb[:s.ne]
        th=0.5*np.log(s.t/np.where(s.d>0,s.d,1)+1e-300)
        w=np.cosh(np.clip(th[a]-th[b],-300,300))           # each relation hosts encounters at the rate the two parts' ticks reach each other
        k=int(np.searchsorted(np.cumsum(w),s.r.random()*w.sum())); k=min(k,s.ne-1)
        i,j=int(a[k]),int(b[k])
        if random.random()<0.5: i,j=j,i
        s.event(i,j)
    def event(s,i,j):
        ti,di,tj,dj=s.t[i],s.d[i],s.t[j],s.d[j]
        if (ti-tj)*(di-dj)<=0: s.c['space']+=1; s.twoview(i,j)
        else:
            s.c['time']+=1; dom,sub=(i,j) if ti>tj else (j,i)
            if s.v in ('oneway','clock','clock_dilated','clock_delta'):
                if random.random()<s.d[dom]/(s.d[dom]+s.d[sub]): s.absorb(dom,sub)
                else: s.crossover(dom,sub)
            else:
                w4=[ti*di,tj*dj,ti*dj,tj*di]; q=random.choices(range(4),weights=w4)[0]
                if q==0: s.absorb(i,j)
                elif q==1: s.absorb(j,i)
                else: s.crossover(i,j)
        s.e+=1
    def snap(s):
        idx=np.flatnonzero(s.alive); eta=np.sqrt(s.t[idx]*s.d[idx]); tot=eta.sum(); srt=np.sort(eta)[::-1]
        pos={k:n for n,k in enumerate(idx)}; lc=[]
        for n,k in enumerate(idx):
            ns=[pos[m] for m in s.nb[k] if m in pos]
            if ns: lc.append(np.log10(eta[n]/np.median(eta[ns])))
        lc=np.array(lc)
        return dict(N=len(idx),largest=srt[0]/tot,top10=srt[:10].sum()/tot,big=int((eta>0.01*tot).sum()),
                    between=float(eta[eta<=0.01*tot].sum()/tot),lc=np.percentile(lc,[25,50,75]),R=1-tot)
if __name__=="__main__":
    variant=sys.argv[1]; seeds=[int(x) for x in sys.argv[2].split(',')]; E=int(sys.argv[3])
    for seed in seeds:
        w=World(200,seed,variant); rows=[]
        for e in range(E+1):
            if e%(E//6)==0:
                sn=w.snap(); rows.append(f"e{e}: N={sn['N']} largest={sn['largest']:.3f} top10={sn['top10']:.3f} parts>1%={sn['big']} between-giants={sn['between']:.3f} local contrast(25/50/75)={np.round(sn['lc'],2)} R={sn['R']:.3f}")
            if w.alive.sum()<2: rows.append(f"COLLAPSED at e{e}"); break
            if len(w.free)<500: rows.append(f"cap at e{e}"); break
            w.step()
        c=w.c; tot=c['space']+c['time']
        print(f"[{variant}, s{seed}] spacelike share={c['space']/max(tot,1):.2f} births={c['births']} deaths={c['deaths']}",flush=True)
        for r in rows: print("    "+r,flush=True)
