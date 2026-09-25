import numpy as np
def colour(edges):
    col={}
    for e in edges:
        used={col[f] for f in col if set(f)&set(e)}; c=0
        while c in used: c+=1
        col[e]=c
    return col,max(col.values())+1
def step_round(tau,dl,rec,sig,edges,col,C,mode):
    for t in range(C):
        for (u,v) in edges:
            if col[(u,v)]!=t: continue
            tu,du,tv,dv=tau[u],dl[u],tau[v],dl[v]
            if mode=='flux':        # one shared flux computed from both records (the form used in A1/A2)
                F=tu*rec[(u,v)][1]-tv*rec[(v,u)][1]; T=tu+tv; D=du+dv
                dl[u]+=F/T; dl[v]-=F/T; tau[u]-=F/D; tau[v]+=F/D
            else:                   # perspectival: each part corrects itself by the exchange law with its own record of the other
                Tu=tu+rec[(u,v)][0]; Du=du+rec[(u,v)][1]; Tv=tv+rec[(v,u)][0]; Dv=dv+rec[(v,u)][1]
                tau[u],dl[u]=Tu*du/Du, Du*tu/Tu
                tau[v],dl[v]=Tv*dv/Dv, Dv*tv/Tv
                s=sig.setdefault((u,v),np.zeros(2)); s+= [tu+tv-tau[u]-tau[v], du+dv-dl[u]-dl[v]]
            rec[(u,v)]=(tv,dv); rec[(v,u)]=(tu,du)
    return tau,dl
def network(seed,N=20):
    rng=np.random.default_rng(seed); edges=[(0,1)]; n=2
    for _ in range(N-2):
        u,v=edges[rng.integers(len(edges))]; c=n; n+=1; edges+=[(u,c),(v,c)]
    return edges,n
def run(mode,spread,rounds,seed=3,eps=0.0,base=None):
    edges,n=network(seed); col,C=colour(edges); rng=np.random.default_rng(seed+1)
    if base is None:
        tau=np.exp(rng.normal(0,spread,n)); dl=np.exp(rng.normal(0,spread,n))
    else: tau,dl=base[0].copy(),base[1].copy()
    if eps: tau*=np.exp(eps*rng.normal(size=n)); dl*=np.exp(eps*rng.normal(size=n))
    rec={}
    for (u,v) in edges: rec[(u,v)]=(tau[v],dl[v]); rec[(v,u)]=(tau[u],dl[u])
    sig={}; T0,D0=tau.sum(),dl.sum(); traj=[]
    for r in range(rounds):
        tau,dl=step_round(tau,dl,rec,sig,edges,col,C,mode)
        if (tau<=0).any() or (dl<=0).any() or not np.isfinite(tau).all(): return None,r
        traj.append(np.concatenate([np.log(tau),np.log(dl)]))
    st=np.array([s for s in sig.values()]) if sig else np.zeros((1,2))
    cons=(tau.sum()+st[:,0].sum()-T0, dl.sum()+st[:,1].sum()-D0)
    th=0.5*np.log(tau/dl)
    return dict(traj=np.array(traj),theta_spread=th.std(),eta_spread=np.log(np.sqrt(tau*dl)).std(),
                relmax=np.abs(st).max()/np.mean(np.sqrt(tau*dl)),cons=cons),rounds
