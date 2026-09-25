import numpy as np, random, math, sys
def run(start_t, start_d, edges0, E=200000, seed=1, cap=20000, every=20000, rule='R1'):
    rng=np.random.default_rng(seed); random.seed(seed)
    tau=np.zeros(cap); dl=np.zeros(cap); alive=np.zeros(cap,bool); born=np.zeros(cap,int)
    nbr=[set() for _ in range(cap)]; free=list(range(cap-1,-1,-1))
    def new(t,d,e):
        k=free.pop(); tau[k]=t; dl[k]=d; alive[k]=True; born[k]=e; nbr[k]=set(); return k
    ids=[new(t,d,0) for t,d in zip(start_t,start_d)]
    for a,b in edges0: nbr[ids[a]].add(ids[b]); nbr[ids[b]].add(ids[a])
    births=deaths=0; out=[]; plife=[]
    for e in range(E+1):
        idx=np.flatnonzero(alive); n=len(idx)
        if e%every==0 or n<2 or n>cap-10:
            eta=np.sqrt(tau[idx]*dl[idx])
            deg=[len(nbr[k]) for k in idx]
            out.append((e,n,births,deaths,1-eta.sum(),eta.max()/eta.sum(),max(deg),np.mean(deg)))
            if n<2 or n>cap-10: break
        # a part acts at a rate set by its continuity; it meets a neighbor in proportion to the neighbor's difference
        pt=tau[idx]; i=idx[np.searchsorted(np.cumsum(pt),rng.random()*pt.sum())]
        nb=list(nbr[i])
        if not nb: continue
        j=random.choices(nb,weights=[dl[k] for k in nb])[0]
        ti,di,tj,dj=tau[i],dl[i],tau[j],dl[j]
        w=[ti*di,tj*dj,ti*dj,tj*di]; k=random.choices(range(4),weights=w)[0]
        if k<2 and rule in ('R1',):
            keep,gone=(i,j) if k==0 else (j,i)
            tau[keep]+=tau[gone]; dl[keep]+=dl[gone]
            for m in nbr[gone]:
                nbr[m].discard(gone)
                if m!=keep: nbr[m].add(keep); nbr[keep].add(m)
            nbr[keep].discard(keep); alive[gone]=False; nbr[gone]=set(); free.append(gone)
            deaths+=1; plife.append(e-born[gone])
        elif k<2:   # bounce
            T=ti+tj; D=di+dj
            tau[i],dl[i]=T*di/D, D*ti/T; tau[j],dl[j]=T*dj/D, D*tj/T
        else:       # crossover birth on the relation (i,j); each child is related to both parents
            tau[i],dl[i],tau[j],dl[j]=ti/2,di/2,tj/2,dj/2
            for (t,d) in ((ti/2,dj/2),(tj/2,di/2)):
                c=new(t,d,e); nbr[c]|={i,j}; nbr[i].add(c); nbr[j].add(c)
            births+=2
    return out,plife
def ring(N,seed):
    r=random.Random(seed); t=[r.uniform(.2,1.8) for _ in range(N)]; d=[r.uniform(.2,1.8) for _ in range(N)]
    T=sum(t); D=sum(d); return [x/T for x in t],[x/D for x in d],[(k,(k+1)%N) for k in range(N)]
if len(sys.argv)==1:
  for seed in (1,2,3):
      t,d,ed=ring(20,seed+20)
      out,pl=run(t,d,ed,seed=seed)
      print(f"LOCAL R1, ring of 20, seed {seed}")
      for e,n,b,dth,rem,top,mxd,avd in out:
          print(f"   e={e:6d} parts={n:5d} births={b:6d} deaths={dth:6d} remainder={rem:.4f} largest share={top:.3f} maxdeg={mxd} meandeg={avd:.2f}")
      if pl: print(f"   part lifetimes: median {np.median(pl):.0f}, mean {np.mean(pl):.0f}")

def ringT(N,spread,seed):
    r=random.Random(seed); th=[r.gauss(0,spread) for _ in range(N)]; m=[r.uniform(.5,1.5) for _ in range(N)]
    t=[a*math.exp(b) for a,b in zip(m,th)]; d=[a*math.exp(-b) for a,b in zip(m,th)]
    T=sum(t); D=sum(d); return [x/T for x in t],[x/D for x in d],[(k,(k+1)%N) for k in range(N)]
if len(sys.argv)>1 and sys.argv[1]=='thermo':
    for label,sp in (("cold",0.01),("hot",1.5)):
        for seed in (1,2):
            t,d,ed=ringT(20,sp,seed+40)
            out,_=run(t,d,ed,E=10**7,seed=seed,cap=8010,every=1000,rule='R2')
            pts=[o for o in out if o[1] in range(990,1100) or o[1] in range(3900,4200) or o[1]>7900 or o[0]==0]
            print(f"LOCAL births+bounces, {label} start, seed {seed}: "+"  ".join(f"N={o[1]}:{o[4]:.4f}" for o in pts[:1]+pts[-3:]))
