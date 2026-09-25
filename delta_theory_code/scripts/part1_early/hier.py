import numpy as np, random, math
def run(start, E=150000, seed=1, burden=True, cap=6000, every=15000, verbose=True):
    rng=np.random.default_rng(seed); random.seed(seed)
    tau=np.zeros(cap); dl=np.zeros(cap); body=np.full(cap,-1); alive=np.zeros(cap,bool); born=np.zeros(cap,int)
    bodies={}; nb=0; npid=0
    for t,d in start:
        tau[npid]=t; dl[npid]=d; alive[npid]=True; body[npid]=nb; bodies[nb]={npid}; nb+=1; npid+=1
    births=deaths=joins=0; plife=[]; bstart={b:0 for b in bodies}; blife=[]
    stats=[]
    def newpart(t,d,b,e):
        nonlocal npid
        # reuse a dead slot
        free=np.flatnonzero(~alive)
        k=free[0]
        tau[k]=t; dl[k]=d; alive[k]=True; body[k]=b; born[k]=e; bodies[b].add(k); return k
    for e in range(E+1):
        idx=np.flatnonzero(alive); n=len(idx)
        if e%every==0 or n<2 or n>cap-10:
            sizes=sorted((len(v) for v in bodies.values()),reverse=True)
            eta=np.sqrt(tau[idx]*dl[idx]).sum()
            stats.append((e,n,len(bodies),sizes[0],sum(1 for s in sizes if s>1),births,deaths,joins,eta))
            if n<2 or n>cap-10: break
        pt=tau[idx]; pd=dl[idx]
        while True:
            i=idx[rng.choice(n,p=pt/pt.sum())]; j=idx[rng.choice(n,p=pd/pd.sum())]
            if i!=j: break
        A=body[i]; B=body[j]
        if A==B:   # internal encounter: selves absorb (death), relation reproduces inside the cluster
            w=[tau[i]*dl[i],tau[j]*dl[j],tau[i]*dl[j],tau[j]*dl[i]]
            k=random.choices(range(4),weights=w)[0]
            if k<2:
                keep,gone=(i,j) if k==0 else (j,i)
                tau[keep]+=tau[gone]; dl[keep]+=dl[gone]; alive[gone]=False; bodies[A].discard(gone)
                deaths+=1; plife.append(e-born[gone])
            else:
                ti,di,tj,dj=tau[i],dl[i],tau[j],dl[j]
                tau[i]/=2; dl[i]/=2; tau[j]/=2; dl[j]/=2
                newpart(ti/2,dj/2,A,e); newpart(tj/2,di/2,A,e); births+=2
        else:      # external encounter between bodies A and B
            mA=list(bodies[A]); mB=list(bodies[B])
            TA,DA=tau[mA].sum(),dl[mA].sum(); TB,DB=tau[mB].sum(),dl[mB].sum()
            w=[TA*DA,TB*DB,TA*DB,TB*DA]
            k=random.choices(range(4),weights=w)[0]
            if k<2:
                act,oth,mact,moth,T,D=(A,B,mA,mB,TA,DA) if k==0 else (B,A,mB,mA,TB,DB)
                coh=(tau[mact]*dl[mact]).sum()/(T*D) if burden else 1.0   # Ch.14: must reconcile its internal relations first
                if random.random()<coh:
                    for m in moth: body[m]=act; bodies[act].add(m)
                    del bodies[oth]; joins+=1; blife.append(e-bstart.pop(oth))
            else:   # the relation between the registering members reproduces; children are new free bodies
                ti,di,tj,dj=tau[i],dl[i],tau[j],dl[j]
                tau[i]/=2; dl[i]/=2; tau[j]/=2; dl[j]/=2
                for (t,d) in ((ti/2,dj/2),(tj/2,di/2)):
                    bodies[nb]=set(); bstart[nb]=e; newpart(t,d,nb,e); nb+=1
                births+=2
        # empty bodies (all members died) are removed
        if A in bodies and not bodies[A]: del bodies[A]; blife.append(e-bstart.pop(A))
    if verbose:
        for s in stats:
            print(f"   e={s[0]:6d} parts={s[1]:5d} bodies={s[2]:5d} largest={s[3]:5d} clusters={s[4]:4d} births={s[5]} deaths={s[6]} joins={s[7]} sum_eta={s[8]:.3f}")
    return stats,plife,blife
random.seed(9); r=[[random.uniform(.2,1.8),random.uniform(.2,1.8)] for _ in range(20)]
T=sum(x[0] for x in r); D=sum(x[1] for x in r); s20=[(x[0]/T,x[1]/D) for x in r]
import sys
mode=sys.argv[1]
if mode=='burden':
    for seed in (1,2):
        print(f"HIERARCHY + CH.14 BURDEN, seed {seed}"); run(s20,seed=seed)
else:
    for seed in (1,2):
        print(f"HIERARCHY, NO BURDEN, seed {seed}"); run(s20,seed=seed,burden=False)
