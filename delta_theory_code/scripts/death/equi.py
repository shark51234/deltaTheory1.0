# Recheck equipartition (Ch. 5 test) under the size-independent activity rule
import numpy as np, statistics as st, math, random
def run(rule,N=60,R=20000,seed=5):
    rng=np.random.default_rng(seed); random.seed(seed)
    t=rng.uniform(.2,1.8,N); d=rng.uniform(.2,1.8,N); t/=t.sum(); d/=d.sum()
    m=np.sqrt(t*d); acc=np.zeros(N); cnt=0
    for r in range(R*N//2):          # same number of exchanges as R rounds of N/2 pairs
        if rule=='registration': wi=t; wj=d
        else: wi=np.sqrt(t/d); wj=np.sqrt(d/t)
        while True:
            i=rng.choice(N,p=wi/wi.sum()); j=rng.choice(N,p=wj/wj.sum())
            if i!=j: break
        T=t[i]+t[j]; D=d[i]+d[j]; ti,di,tj,dj=t[i],d[i],t[j],d[j]
        t[i],d[i]=T*di/D,D*ti/T; t[j],d[j]=T*dj/D,D*tj/T
        if r>R*N//4 and r%N==0:
            E=(t+d)/2; p=(t-d)/2; acc+=p*p/E; cnt+=1
    pv=acc/cnt; o=np.argsort(m); k=N//3
    return pv[o[:k]].mean(),pv[o[-k:]].mean(),pv.std()/pv.mean()
for rule in ('registration','size-independent'):
    lo,hi,sp=run(rule)
    print(f"{rule:17s}: <pv> lightest third={lo:.5f} heaviest third={hi:.5f} relative spread={sp:.3f}")
