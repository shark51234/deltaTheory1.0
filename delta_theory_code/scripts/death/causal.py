import numpy as np, random, sys
class World:
    def __init__(s,N0,seed,variant,cap=80000):
        s.r=np.random.default_rng(seed); random.seed(seed); s.v=variant
        s.t=np.zeros(cap); s.d=np.zeros(cap); s.alive=np.zeros(cap,bool); s.born=np.zeros(cap,dtype=np.int64)
        s.nb=[set() for _ in range(cap)]; s.free=list(range(cap-1,-1,-1)); s.e=0
        s.c=dict(space=0,time=0,births=0,deaths=0,reldeaths=0); s.touched=set(); s.life=[]
        t=s.r.uniform(.2,1.8,N0); d=s.r.uniform(.2,1.8,N0); t/=t.sum(); d/=d.sum()
        ks=[s.new(a,b) for a,b in zip(t,d)]
        for x in range(N0): s.link(ks[x],ks[(x+1)%N0])
    def new(s,t,d):
        k=s.free.pop(); s.t[k]=t; s.d[k]=d; s.alive[k]=True; s.nb[k]=set(); s.born[k]=s.e; s.touched.add(k); return k
    def enclosed(s,f):
        nb=s.nb[f]
        if not nb: return False
        return all(s.t[a]>=s.t[f] and s.d[a]>=s.d[f] for a in nb)
    def relational_death(s):
        # a part contained by every neighbour can register none of them: it has no perspective of its own
        queue=set()
        for k in s.touched:
            if s.alive[k]: queue.add(k); queue|=s.nb[k]
        s.touched=set()
        while queue:
            f=queue.pop()
            if not s.alive[f] or not s.enclosed(f): continue
            nbrs=list(s.nb[f])
            if getattr(s,'spread',False):
                # every neighbour takes in the share of f it registers (proportional to its continuity); the neighbours become related
                tot=sum(s.t[a] for a in nbrs)
                for a in nbrs:
                    wa=s.t[a]/tot; s.t[a]+=wa*s.t[f]; s.d[a]+=wa*s.d[f]; s.nb[a].discard(f)
                for x in range(len(nbrs)):
                    for y in range(x+1,len(nbrs)): s.link(nbrs[x],nbrs[y])
                s.nb[f]=set(); s.alive[f]=False; s.free.append(f); s.life.append(s.e-s.born[f]); s.c['reldeaths']+=1
            else:
                a=max(nbrs,key=lambda m:s.t[m])          # its strongest registrant takes it in
                s.absorb(a,f); s.c['deaths']-=1; s.c['reldeaths']+=1
            queue|=set(nbrs)
    def link(s,a,b):
        if a!=b: s.nb[a].add(b); s.nb[b].add(a)
    def absorb(s,keep,gone):
        s.t[keep]+=s.t[gone]; s.d[keep]+=s.d[gone]
        for m in list(s.nb[gone]):
            s.nb[m].discard(gone)
            if m!=keep: s.link(keep,m)
        s.nb[gone]=set(); s.alive[gone]=False; s.free.append(gone)
        s.c['deaths']+=1; s.life.append(s.e-s.born[gone])
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
        idx=np.flatnonzero(s.alive)
        if getattr(s,'inertia',False):   # size-independent activity: initiate ~ tau/eta = e^theta, partner ~ delta/eta = e^-theta
            pt=np.sqrt(s.t[idx]/s.d[idx])
        else:
            pt=s.t[idx]
        i=int(idx[np.searchsorted(np.cumsum(pt),s.r.random()*pt.sum())])
        nb=list(s.nb[i])
        if not nb: s.e+=1; return
        if getattr(s,'inertia',False):
            j=random.choices(nb,weights=[np.sqrt(s.d[k]/s.t[k]) for k in nb])[0]
        else:
            j=random.choices(nb,weights=[s.d[k] for k in nb])[0]
        ti,di,tj,dj=s.t[i],s.d[i],s.t[j],s.d[j]
        if s.v=='twoview' or (ti-tj)*(di-dj)<=0:      # relation dominates (spacelike pair): both views act
            s.c['space']+=1; s.twoview(i,j)
        else:                                          # selves dominate (timelike pair)
            s.c['time']+=1
            dom,sub=(i,j) if ti>tj else (j,i)
            if s.v=='selves':                          # the selves decide: pick an entry in proportion to size
                w=[ti*di,tj*dj,ti*dj,tj*di]; k=random.choices(range(4),weights=w)[0]
                if k==0: s.absorb(i,j)
                elif k==1: s.absorb(j,i)
                else: s.crossover(i,j)
            else:                                      # 'oneway': only the containing part registers; its row decides
                vd=s.d[dom]/(s.d[dom]+s.d[sub])
                if random.random()<vd: s.absorb(dom,sub)
                else: s.crossover(dom,sub)
        s.touched|={i,j}
        if getattr(s,'reldeath',False): s.relational_death()
        else: s.touched=set()
        s.e+=1
    def snap(s):
        idx=np.flatnonzero(s.alive); t=s.t[idx]; d=s.d[idx]; eta=np.sqrt(t*d); tot=eta.sum()
        big=np.sort(eta)[::-1]
        med=np.median(eta); rel=eta/med
        b=np.logspace(np.log10(rel.min()),np.log10(rel.max())*1.000001,31); h,_=np.histogram(rel,bins=b)
        c=np.sqrt(b[:-1]*b[1:]); dens=h/(np.diff(b)*len(rel)); m=(c>2)&(h>=5)
        slope=np.polyfit(np.log10(c[m]),np.log10(dens[m]),1)[0] if m.sum()>=4 else float('nan')
        return dict(N=len(idx),R=1-tot,top1=big[0]/tot,top10=big[:10].sum()/tot,n1pct=int((eta>0.01*tot).sum()),
                    span=np.log10(rel.max()),slope=slope)
if __name__=="__main__":
    variant=sys.argv[1]; seeds=[int(x) for x in sys.argv[2].split(',')]; E=int(sys.argv[3])
    inertia='inertia' in sys.argv[4:]; reldeath=('reldeath' in sys.argv[4:]) or ('spread' in sys.argv[4:]); spread='spread' in sys.argv[4:]
    for seed in seeds:
        w=World(200,seed,variant); w.inertia=inertia; w.reldeath=reldeath; w.spread=spread; out=[]
        for e in range(E+1):
            n=int(w.alive.sum())
            if e%(E//6)==0:
                sn=w.snap(); out.append(f"e{e}: N={sn['N']}, R={sn['R']:.3f}, largest={sn['top1']:.3f}, top10={sn['top10']:.3f}, parts>1%={sn['n1pct']}, span=10^{sn['span']:.2f}, tail={sn['slope']:.2f}")
            if n<2: out.append(f"COLLAPSED at e{e}"); break
            if len(w.free)<500: out.append(f"cap at e{e}"); break
            w.step()
        c=w.c; tot=c['space']+c['time']
        lt=np.array(w.life) if w.life else np.array([0])
        print(f"[{variant}{'+inertia' if inertia else ''}{'+reldeath' if reldeath and not spread else ''}{'+spread-death' if spread else ''} s{seed}] spacelike share={c['space']/max(tot,1):.2f} births={c['births']} deaths={c['deaths']} relational deaths={c['reldeaths']} median life={np.median(lt):.0f}",flush=True)
        for o in out: print("    "+o,flush=True)
