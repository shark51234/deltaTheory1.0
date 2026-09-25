import numpy as np, sys, random
class Net:
    def __init__(s,N0,seed,records=True,cap=60000):
        s.r=np.random.default_rng(seed); random.seed(seed); s.records=records; s.cap=cap
        s.t=np.zeros(cap); s.d=np.zeros(cap); s.alive=np.zeros(cap,bool); s.id=np.zeros(cap,dtype=np.int64)
        s.nb=[set() for _ in range(cap)]; s.free=list(range(cap-1,-1,-1)); s.nid=0; s.rec={}; s.e=0
        t=s.r.uniform(.2,1.8,N0); d=s.r.uniform(.2,1.8,N0); t/=t.sum(); d/=d.sum()
        ks=[s.new(a,b) for a,b in zip(t,d)]
        for x in range(N0): s.link(ks[x],ks[(x+1)%N0])
        s.st=dict(births=0,deaths=0,stale=0,void=0,emitted=0.0,light_absorbed=0.0)
    def new(s,t,d):
        k=s.free.pop(); s.t[k]=max(t,0.); s.d[k]=max(d,0.); s.alive[k]=True; s.id[k]=s.nid; s.nid+=1; s.nb[k]=set(); return k
    def link(s,a,b):
        if a!=b: s.nb[a].add(b); s.nb[b].add(a)
    def remove(s,k,heir=None):
        for m in list(s.nb[k]):
            s.nb[m].discard(k)
            if heir is not None and m!=heir: s.link(heir,m)
        s.nb[k]=set(); s.alive[k]=False; s.free.append(k)
    def massive(s,k): return s.t[k]>0 and s.d[k]>0
    def take_local_light(s,a,b,comp,amount):
        arr=s.t if comp==0 else s.d; oth=s.d if comp==0 else s.t
        pool=[k for k in (s.nb[a]|s.nb[b]) if s.alive[k] and arr[k]>0 and oth[k]==0]
        if sum(arr[k] for k in pool)<amount: return False
        random.shuffle(pool); need=amount
        for k in pool:
            if arr[k]<=need: need-=arr[k]; arr[k]=0.; s.remove(k,heir=a)
            else: arr[k]-=need; need=0.
            if need<=0: break
        return True
    def step(s,q):
        idx=np.flatnonzero(s.alive); pt=s.t[idx]
        if pt.sum()<=0: return False
        i=int(idx[np.searchsorted(np.cumsum(pt),s.r.random()*pt.sum())])
        nb=[k for k in s.nb[i] if s.d[k]>0]
        if not nb: s.e+=1; return True
        j=random.choices(nb,weights=[s.d[k] for k in nb])[0]
        ti,di,tj,dj=s.t[i],s.d[i],s.t[j],s.d[j]; ii,jj=s.id[i],s.id[j]
        w=[ti*di,tj*dj,ti*dj,tj*di]; k=random.choices(range(4),weights=w)[0]
        bm=s.massive(i) and s.massive(j)
        if k<2 and random.random()<q:
            keep,gone=(i,j) if k==0 else (j,i)
            if s.massive(gone): s.st['deaths']+=1
            else: s.st['light_absorbed']+=s.t[gone]+s.d[gone]
            s.t[keep]+=s.t[gone]; s.d[keep]+=s.d[gone]; s.remove(gone,heir=keep)
        elif k<2:
            if s.records and bm:
                tbr,dbr=s.rec.get((ii,jj),(tj,dj)); tar,dar=s.rec.get((jj,ii),(ti,di))
            else: tbr,dbr,tar,dar=tj,dj,ti,di
            Ta=ti+tbr; Da=di+dbr; Tb=tar+tj; Db=dar+dj
            ti2,di2=Ta*di/Da,Da*ti/Ta; tj2,dj2=Tb*dj/Db,Db*tj/Tb
            rt=(ti+tj)-(ti2+tj2); rd=(di+dj)-(di2+dj2)
            if abs(rt)>1e-15 or abs(rd)>1e-15: s.st['stale']+=1
            ok=True; taken_t=0.
            if rt<-1e-15:
                ok=s.take_local_light(i,j,0,-rt); taken_t=-rt if ok else 0.
            if ok and rd<-1e-15:
                ok=s.take_local_light(i,j,1,-rd)
                if not ok and taken_t>0: c=s.new(taken_t,0.); s.link(c,i); s.link(c,j)   # refund
            if not ok: s.st['void']+=1
            else:
                s.t[i],s.d[i],s.t[j],s.d[j]=ti2,di2,tj2,dj2
                for (a,b) in ((rt,0.),(0.,rd)):
                    if a>1e-15 or b>1e-15:
                        c=s.new(a,b); s.link(c,i); s.link(c,j); s.st['emitted']+=a+b
            if bm: s.rec[(ii,jj)]=(tj,dj); s.rec[(jj,ii)]=(ti,di)
        else:
            s.t[i],s.d[i],s.t[j],s.d[j]=ti/2,di/2,tj/2,dj/2
            for (a,b) in ((ti/2,dj/2),(tj/2,di/2)):
                if a>0 or b>0:
                    c=s.new(a,b); s.link(c,i); s.link(c,j)
                    if a>0 and b>0: s.st['births']+=1
            if bm: s.rec[(ii,jj)]=(tj,dj); s.rec[(jj,ii)]=(ti,di)
        s.e+=1; return True
    def report(s):
        idx=np.flatnonzero(s.alive); t=s.t[idx]; d=s.d[idx]; m=(t>0)&(d>0)
        eta=np.sqrt(t[m]*d[m]); light=(t[~m].sum()+d[~m].sum())/2
        return int(m.sum()),int((~m).sum()),(float(eta.max()/eta.sum()) if len(eta) else float('nan')),float(light)
if __name__=="__main__":
    q=float(sys.argv[1]); rec=sys.argv[2]=="rec"; E=int(sys.argv[3]); seeds=[int(x) for x in sys.argv[4].split(',')]; N0=int(sys.argv[5])
    for seed in seeds:
        u=Net(N0,seed,records=rec); line=[]
        for e in range(E+1):
            if e%(E//5)==0:
                M,L,g,lt=u.report(); line.append(f"e{e}:M={M},L={L},giant={g:.2f},light={lt:.3f}")
            M=int(sum(1 for k in np.flatnonzero(u.alive) if u.massive(k))) if e%500==0 else 2
            if e%500==0 and M<2:
                line.append(f"collapsed(e={e})"); break
            if len(u.free)<100: line.append(f"cap(e={e})"); break
            u.step(q)
        print(f"q={q} {'REC' if rec else 'no-rec'} s{seed}: "+" | ".join(line)+f" || {u.st}",flush=True)
