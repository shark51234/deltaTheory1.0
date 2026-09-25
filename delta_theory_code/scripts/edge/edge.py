import numpy as np, sys, json
class Universe:
    def __init__(s, N0, seed, cap=200000):
        s.rng=np.random.default_rng(seed)
        s.t=np.zeros(cap); s.d=np.zeros(cap); s.born=np.zeros(cap,dtype=np.int64)
        t=s.rng.uniform(.2,1.8,N0); d=s.rng.uniform(.2,1.8,N0)
        s.t[:N0]=t/t.sum(); s.d[:N0]=d/d.sum(); s.n=N0; s.e=0
        s.lifetimes=[]; s.births=0; s.deaths=0
    def kill(s,k):
        s.lifetimes.append(s.e-s.born[k]); last=s.n-1
        s.t[k]=s.t[last]; s.d[k]=s.d[last]; s.born[k]=s.born[last]; s.n-=1; s.deaths+=1
    def add(s,t,d):
        k=s.n; s.t[k]=t; s.d[k]=d; s.born[k]=s.e; s.n+=1; s.births+=1
    def step(s,q):
        n=s.n; ct=np.cumsum(s.t[:n]); cd=np.cumsum(s.d[:n])
        while True:
            i=int(np.searchsorted(ct,s.rng.random()*ct[-1])); j=int(np.searchsorted(cd,s.rng.random()*cd[-1]))
            i=min(i,n-1); j=min(j,n-1)
            if i!=j: break
        ti,di,tj,dj=s.t[i],s.d[i],s.t[j],s.d[j]
        w=np.array([ti*di,tj*dj,ti*dj,tj*di]); r=s.rng.random()*w.sum()
        k=0 if r<w[0] else 1 if r<w[0]+w[1] else 2
        if k<2:
            if s.rng.random()<q:        # the acting self absorbs the other
                keep,gone=(i,j) if k==0 else (j,i)
                s.t[keep]+=s.t[gone]; s.d[keep]+=s.d[gone]; s.kill(gone)
            else:                        # bounce
                T=ti+tj; D=di+dj
                s.t[i],s.d[i]=T*di/D, D*ti/T; s.t[j],s.d[j]=T*dj/D, D*tj/T
        else:                            # crossover birth
            s.t[i],s.d[i],s.t[j],s.d[j]=ti/2,di/2,tj/2,dj/2
            s.add(ti/2,dj/2); s.add(tj/2,di/2)
        s.e+=1
if __name__=="__main__":
    mode=sys.argv[1]
    if mode=="scan":
        N0=int(sys.argv[2]); E=int(sys.argv[3]); qs=[float(x) for x in sys.argv[4].split(',')]
        for q in qs:
            U=Universe(N0,seed=7); traj=[]
            for e in range(E):
                if e%(E//10)==0: traj.append(U.n)
                if U.n<2 or U.n>150000: break
                U.step(q)
            traj.append(U.n)
            print(f"q={q:.3f}: N over time = {traj}", flush=True)
