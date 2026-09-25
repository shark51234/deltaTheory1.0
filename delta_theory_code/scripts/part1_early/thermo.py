import numpy as np, random, math
def run(start, seed, cap=16000, marks=(1000,4000,8000,12000,16000)):
    rng=np.random.default_rng(seed); random.seed(seed)
    tau=list(start[0]); dl=list(start[1]); out=[]; mk=list(marks)
    rem0=1-sum(math.sqrt(a*b) for a,b in zip(tau,dl))
    out.append((len(tau),rem0))
    while len(tau)<cap:
        t=np.array(tau); d=np.array(dl); n=len(t)
        while True:
            i=rng.choice(n,p=t/t.sum()); j=rng.choice(n,p=d/d.sum())
            if i!=j: break
        w=[t[i]*d[i],t[j]*d[j],t[i]*d[j],t[j]*d[i]]
        k=random.choices(range(4),weights=w)[0]
        ti,di,tj,dj=tau[i],dl[i],tau[j],dl[j]
        if k<2:   # bounce (elastic swap)
            T=ti+tj; D=di+dj
            tau[i],dl[i]=T*di/D, D*ti/T; tau[j],dl[j]=T*dj/D, D*tj/T
        else:     # crossover birth
            tau[i],dl[i],tau[j],dl[j]=ti/2,di/2,tj/2,dj/2
            tau+= [ti/2,tj/2]; dl+=[dj/2,di/2]
        if mk and len(tau)>=mk[0]:
            out.append((len(tau),1-sum(math.sqrt(a*b) for a,b in zip(tau,dl)))); mk.pop(0)
    return out
def mk(N,spread,seed):
    r=random.Random(seed); th=[r.gauss(0,spread) for _ in range(N)]; m=[r.uniform(.5,1.5) for _ in range(N)]
    t=[a*math.exp(b) for a,b in zip(m,th)]; d=[a*math.exp(-b) for a,b in zip(m,th)]
    T=sum(t); D=sum(d); return ([x/T for x in t],[x/D for x in d])
for label,spread in (("cold start",0.01),("hot start",1.5)):
    for seed in (3,):
        s=mk(20,spread,seed+10)
        o=run(s,seed)
        print(f"{label} seed {seed}: "+"  ".join(f"N={n}:{rem:.4f}" for n,rem in o))
