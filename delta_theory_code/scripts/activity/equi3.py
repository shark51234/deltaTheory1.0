import numpy as np
def run(N=60,R=8000,seed=5):
    rng=np.random.default_rng(seed)
    t=rng.uniform(.2,1.8,N); d=rng.uniform(.2,1.8,N); t/=t.sum(); d/=d.sum()
    m=np.sqrt(t*d); acc=np.zeros(N); cnt=0
    for r in range(R*N//2):
        th=0.5*np.log(t/d); i=rng.integers(N)
        w=np.exp(th[i]-th); w[i]=0; j=rng.choice(N,p=w/w.sum())
        T=t[i]+t[j]; D=d[i]+d[j]; ti,di,tj,dj=t[i],d[i],t[j],d[j]
        t[i],d[i]=T*di/D,D*ti/T; t[j],d[j]=T*dj/D,D*tj/T
        if r>R*N//4 and r%N==0:
            E=(t+d)/2; p=(t-d)/2; acc+=p*p/E; cnt+=1
    pv=acc/cnt; o=np.argsort(m); k=N//3
    return pv[o[:k]].mean(),pv[o[-k:]].mean(),pv.std()/pv.mean()
lo,hi,sp=run()
print(f"equal clocks + propagating difference: <pv> lightest third={lo:.5f} heaviest third={hi:.5f} relative spread={sp:.3f}")
