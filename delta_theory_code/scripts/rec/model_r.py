import numpy as np, sys
class U:
    def __init__(s,N0,seed,cap=400000,records=True):
        s.r=np.random.default_rng(seed); s.cap=cap; s.records=records
        s.t=np.zeros(cap); s.d=np.zeros(cap); s.id=np.zeros(cap,dtype=np.int64); s.n=0; s.nid=0
        t=s.r.uniform(.2,1.8,N0); d=s.r.uniform(.2,1.8,N0); t/=t.sum(); d/=d.sum()
        for a,b in zip(t,d): s.add(a,b)
        s.rec={}; s.e=0; s.stats=dict(births=0,deaths=0,stale=0,void=0,emitted=0.0,absorbed_light=0.0)
    def add(s,t,d):
        if t<=0 and d<=0: return
        k=s.n; s.t[k]=max(t,0.0); s.d[k]=max(d,0.0); s.id[k]=s.nid; s.nid+=1; s.n+=1
    def kill(s,k):
        last=s.n-1; s.t[k]=s.t[last]; s.d[k]=s.d[last]; s.id[k]=s.id[last]; s.n-=1
    def massive(s): return (s.t[:s.n]>0)&(s.d[:s.n]>0)
    def take_light(s,comp,amount):
        # consume 'amount' of pure-continuity (comp=0) or pure-difference (comp=1) quanta; return False if not enough
        arr = s.t if comp==0 else s.d; other = s.d if comp==0 else s.t
        q=np.flatnonzero((arr[:s.n]>0)&(other[:s.n]==0))
        if arr[q].sum()<amount: return False
        s.r.shuffle(q); need=amount; dead=[]
        for k in q:
            if arr[k]<=need: need-=arr[k]; arr[k]=0; dead.append(k)
            else: arr[k]-=need; need=0
            if need<=0: break
        for k in sorted(dead,reverse=True): s.kill(k)
        return True
    def step(s,q):
        n=s.n; ct=np.cumsum(s.t[:n]); cd=np.cumsum(s.d[:n])
        for _ in range(100):
            i=min(int(np.searchsorted(ct,s.r.random()*ct[-1])),n-1); j=min(int(np.searchsorted(cd,s.r.random()*cd[-1])),n-1)
            if i!=j: break
        else: return
        ti,di,tj,dj=s.t[i],s.d[i],s.t[j],s.d[j]; ii,jj=s.id[i],s.id[j]
        w=np.array([ti*di,tj*dj,ti*dj,tj*di]); tot=w.sum()
        if tot<=0: return
        x=s.r.random()*tot; k=0 if x<w[0] else 1 if x<w[0]+w[1] else 2
        both_massive = ti>0 and di>0 and tj>0 and dj>0
        if k<2 and s.r.random()<q:          # a self absorbs the other
            keep,gone=(i,j) if k==0 else (j,i)
            s.t[keep]+=s.t[gone]; s.d[keep]+=s.d[gone]
            if s.t[gone]>0 and s.d[gone]>0: s.stats['deaths']+=1
            else: s.stats['absorbed_light']+=s.t[gone]+s.d[gone]
            s.kill(gone)
        elif k<2:                            # bounce: each side corrects itself from its record of the other
            if s.records and both_massive:
                tbr,dbr=s.rec.get((ii,jj),(tj,dj)); tar,dar=s.rec.get((jj,ii),(ti,di))
            else: tbr,dbr,tar,dar=tj,dj,ti,di
            Ta=ti+tbr; Da=di+dbr; Tb=tar+tj; Db=dar+dj
            ti2,di2=Ta*di/Da, Da*ti/Ta; tj2,dj2=Tb*dj/Db, Db*tj/Tb
            rt=(ti+tj)-(ti2+tj2); rd=(di+dj)-(di2+dj2)
            if abs(rt)>1e-15 or abs(rd)>1e-15: s.stats['stale']+=1
            ok=True
            if rt<-1e-15: ok=s.take_light(0,-rt)
            if ok and rd<-1e-15:
                ok=s.take_light(1,-rd)
                # (if the second take fails after the first succeeded, the taken light is lost to the pair; keep simple: refund)
                if not ok and rt<-1e-15: s.add(-rt,0.0)
            if not ok: s.stats['void']+=1
            else:
                # indices may have shifted if quanta were removed; locate by id
                ia=np.flatnonzero(s.id[:s.n]==ii)[0]; ja=np.flatnonzero(s.id[:s.n]==jj)[0]
                s.t[ia],s.d[ia],s.t[ja],s.d[ja]=ti2,di2,tj2,dj2
                if rt>1e-15: s.add(rt,0.0); s.stats['emitted']+=rt
                if rd>1e-15: s.add(0.0,rd); s.stats['emitted']+=rd
            if both_massive: s.rec[(ii,jj)]=(tj,dj); s.rec[(jj,ii)]=(ti,di)
        else:                                # the relation reproduces (crossover)
            s.t[i],s.d[i],s.t[j],s.d[j]=ti/2,di/2,tj/2,dj/2
            before=s.n; s.add(ti/2,dj/2); s.add(tj/2,di/2)
            s.stats['births']+=sum(1 for c in (ti/2*dj/2, tj/2*di/2) if c>0)
            if both_massive: s.rec[(ii,jj)]=(tj,dj); s.rec[(jj,ii)]=(ti,di)
        s.e+=1
    def report(s):
        m=s.massive(); eta=np.sqrt(s.t[:s.n][m]*s.d[:s.n][m])
        light=(s.t[:s.n][~m].sum()+s.d[:s.n][~m].sum())/2
        return dict(e=s.e,massive=int(m.sum()),quanta=int((~m).sum()),sum_eta=float(eta.sum()),
                    giant=float(eta.max()/eta.sum()) if len(eta) else float('nan'),light_energy=float(light))
if __name__=="__main__":
    q=float(sys.argv[1]); rec=sys.argv[2]=="rec"; E=int(sys.argv[3]); seeds=[int(x) for x in sys.argv[4].split(',')]
    for seed in seeds:
        u=U(1000,seed,records=rec); marks=set(range(0,E+1,E//6))
        line=[]
        for e in range(E+1):
            if e in marks:
                r=u.report(); line.append(f"e{e}: M={r['massive']} L={r['quanta']} giant={r['giant']:.2f} light={r['light_energy']:.3f}")
            if u.massive().sum()<2 and u.n-u.massive().sum()==0: line.append(f"collapsed at {u.e}"); break
            if u.n>150000: line.append("cap"); break
            u.step(q)
        print(f"q={q} {'records' if rec else 'no records'} seed={seed}: "+" | ".join(line)+f" || stats {u.stats}",flush=True)
