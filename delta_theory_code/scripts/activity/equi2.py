# Equipartition under the derived rule: a pair meets at a rate proportional to cosh of their relative rapidity
import numpy as np
def run(rule,N=60,R=20000,seed=5):
    rng=np.random.default_rng(seed)
    t=rng.uniform(.2,1.8,N); d=rng.uniform(.2,1.8,N); t/=t.sum(); d/=d.sum()
    m=np.sqrt(t*d); acc=np.zeros(N); cnt=0; iu=np.triu_indices(N,1)
    for r in range(R*N//2):
        th=0.5*np.log(t/d)
        if rule=='cosh': w=np.cosh(th[iu[0]]-th[iu[1]])
        else: w=t[iu[0]]*d[iu[1]]+t[iu[1]]*d[iu[0]]
        k=rng.choice(len(w),p=w/w.sum()); i,j=iu[0][k],iu[1][k]
        T=t[i]+t[j]; D=d[i]+d[j]; ti,di,tj,dj=t[i],d[i],t[j],d[j]
        t[i],d[i]=T*di/D,D*ti/T; t[j],d[j]=T*dj/D,D*tj/T
        if r>R*N//4 and r%N==0:
            E=(t+d)/2; p=(t-d)/2; acc+=p*p/E; cnt+=1
    pv=acc/cnt; o=np.argsort(m); k=N//3
    return pv[o[:k]].mean(),pv[o[-k:]].mean(),pv.std()/pv.mean()
for rule in ('registration','cosh'):
    lo,hi,sp=run(rule,R=8000)
    print(f"{rule:12s}: <pv> lightest third={lo:.5f} heaviest third={hi:.5f} relative spread={sp:.3f}",flush=True)
