import numpy as np
from perspectival import colour, network
def simulate(a,seed=3,N=24,R=6000,warm=500):
    edges,n=network(seed,N); col,C=colour(edges)
    nb=[[] for _ in range(n)]
    for u,v in edges: nb[u].append(v); nb[v].append(u)
    tau=np.ones(n); dl=np.ones(n)
    tau[0]*=np.exp(a); dl[0]*=np.exp(-a)            # a small, localized kick to one part's balance
    rel={(u,v):(tau[u]/(tau[u]+tau[v]),dl[u]/(dl[u]+dl[v])) for (u,v) in edges}
    th_sum=np.zeros(n); th2=np.zeros(n); rate=np.zeros(n); pred=np.zeros(n); absd=np.zeros(n); cnt=0; Q=[]
    for r in range(R):
        for t in range(C):
            for (u,v) in edges:
                if col[(u,v)]!=t: continue
                T=tau[u]+tau[v]; D=dl[u]+dl[v]; xu,yu=rel[(u,v)]; rel[(u,v)]=(tau[u]/T,dl[u]/D)
                tau[u],tau[v]=T*yu,T*(1-yu); dl[u],dl[v]=D*xu,D*(1-xu)
            if r>=warm:
                th=0.5*np.log((tau/tau.sum())/(dl/dl.sum()))
                th_sum+=th; th2+=th**2; cnt+=1
                for k in range(n):
                    d=th[nb[k]]-th[k]
                    rate[k]+=np.exp(d).sum()            # how strongly k's neighbours register k: sum of Doppler factors e^(theta_i - theta_k)
                    pred[k]+=0.5*(d**2).sum()             # second-order prediction for the excess over the resting rate
                    absd[k]+=np.abs(d).sum()
        if r>=warm and r%100==0: Q.append((th**2).sum())
    deg=np.array([len(x) for x in nb])
    return dict(excess=rate/cnt-deg,pred=pred/cnt,absd=absd/cnt,th2=th2/cnt,mean_th=th_sum/cnt,Q=np.array(Q))
res={}
for a in (0.01,0.02,0.04):
    res[a]=simulate(a)
    e,p=res[a]['excess'],res[a]['pred']
    slope=np.polyfit(p,e,1)[0]; corr=np.corrcoef(p,e)[0,1]
    Q=res[a]['Q']
    print(f"kick {a}: total excess registration {e.sum():.3e}; matches 0.5*sum<(dtheta)^2> part by part: correlation {corr:.4f}, slope {slope:.3f}; "
          f"sum of theta^2 over time: mean {Q.mean():.3e}, relative spread {Q.std()/Q.mean():.2f}; mean theta at the kicked part {res[a]['mean_th'][0]:+.2e}")
e1,e2,e4=(res[a]['excess'].sum() for a in (0.01,0.02,0.04))
print(f"scaling of the excess with kick size: x{e2/e1:.2f} when doubled, x{e4/e1:.2f} when quadrupled (squared amplitude predicts x4 and x16; plain amplitude x2 and x4)")
# does the excess follow squared or plain amplitude across parts?
for a in (0.02,):
    e=res[a]['excess']; sq=res[a]['pred']; lin=res[a]['absd']
    m=(e>0)&(sq>0)&(lin>0)
    s_sq=np.polyfit(np.log(sq[m]),np.log(e[m]),1)[0]; s_lin=np.polyfit(np.log(lin[m]),np.log(e[m]),1)[0]
    print(f"across parts (kick {a}): log-log slope of excess against squared amplitude {s_sq:.2f} (1 = proportional); against plain amplitude {s_lin:.2f}")
