import numpy as np, random, sys
class World:
    """Local relational network, rule S1(q), records on relations.
       mode 'none': stale corrections that need absent light are void (previous model)
       mode 'a'   : as 'none', but the universe starts with a fraction f of itself as light
       mode 'b'   : residues are stored on the relation itself (signed); nothing is void"""
    def __init__(s,N0,seed,mode,f=0.0,cap=40000):
        s.r=np.random.default_rng(seed); random.seed(seed); s.mode=mode; s.cap=cap
        s.t=np.zeros(cap); s.d=np.zeros(cap); s.alive=np.zeros(cap,bool); s.id=np.zeros(cap,dtype=np.int64)
        s.nb=[set() for _ in range(cap)]; s.free=list(range(cap-1,-1,-1)); s.nid=0
        s.rec={}; s.rel={}; s.e=0
        s.st=dict(births=0,deaths=0,stale=0,void=0,blocked=0,emitted=0.0)
        t=s.r.uniform(.2,1.8,N0); d=s.r.uniform(.2,1.8,N0); t*= (1-f)/t.sum(); d*=(1-f)/d.sum()
        ks=[s.new(a,b) for a,b in zip(t,d)]
        for x in range(N0): s.link(ks[x],ks[(x+1)%N0])
        if f>0:
            for x in range(N0):
                for (a,b) in ((f/N0,0.),(0.,f/N0)):
                    c=s.new(a,b); s.link(c,ks[x]); s.link(c,ks[(x+1)%N0])
    def new(s,t,d):
        k=s.free.pop(); s.t[k]=max(t,0.); s.d[k]=max(d,0.); s.alive[k]=True; s.id[k]=s.nid; s.nid+=1; s.nb[k]=set(); return k
    def link(s,a,b):
        if a!=b: s.nb[a].add(b); s.nb[b].add(a)
    def key(s,a,b): x,y=s.id[a],s.id[b]; return (x,y) if x<y else (y,x)
    def massive(s,k): return s.t[k]>0 and s.d[k]>0
    def remove(s,k,heir=None):
        for m in list(s.nb[k]):
            s.nb[m].discard(k)
            if heir is not None and m!=heir:
                s.link(heir,m)
                if s.mode=='b':
                    old=s.rel.pop(s.key(k,m),None)
                    if old is not None:
                        kk=s.key(heir,m); cur=s.rel.get(kk,[0.,0.]); s.rel[kk]=[cur[0]+old[0],cur[1]+old[1]]
        s.nb[k]=set(); s.alive[k]=False; s.free.append(k)
    def take_light(s,a,b,comp,amount):
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
        i=int(idx[np.searchsorted(np.cumsum(pt),s.r.random()*pt.sum())])
        nb=[k for k in s.nb[i] if s.d[k]>0]
        if not nb: s.e+=1; return
        j=random.choices(nb,weights=[s.d[k] for k in nb])[0]
        ti,di,tj,dj=s.t[i],s.d[i],s.t[j],s.d[j]; ii,jj=s.id[i],s.id[j]
        if getattr(s,'sel','pair')=='row':      # the initiator decides from its own row of the matrix
            k=0 if random.random()<di/(di+dj) else 2
        else:
            w=[ti*di,tj*dj,ti*dj,tj*di]; k=random.choices(range(4),weights=w)[0]
        bm=s.massive(i) and s.massive(j)
        if k<2 and random.random()<q:                       # a self absorbs the other
            keep,gone=(i,j) if k==0 else (j,i)
            add_t,add_d=s.t[gone],s.d[gone]
            if s.mode=='b':
                sig=s.rel.get(s.key(keep,gone),[0.,0.])
                add_t+=sig[0]; add_d+=sig[1]
                if s.t[keep]+add_t<=0 or s.d[keep]+add_d<=0:   # a debt on the relation forbids the merger
                    s.st['blocked']+=1; s.e+=1; return
                s.rel.pop(s.key(keep,gone),None)
            if s.massive(gone): s.st['deaths']+=1
            s.t[keep]+=add_t; s.d[keep]+=add_d; s.remove(gone,heir=keep)
        elif k<2:                                           # bounce, each side acting on its record
            if bm: tbr,dbr=s.rec.get((ii,jj),(tj,dj)); tar,dar=s.rec.get((jj,ii),(ti,di))
            else: tbr,dbr,tar,dar=tj,dj,ti,di
            Ta=ti+tbr; Da=di+dbr; Tb=tar+tj; Db=dar+dj
            ti2,di2=Ta*di/Da,Da*ti/Ta; tj2,dj2=Tb*dj/Db,Db*tj/Tb
            rt=(ti+tj)-(ti2+tj2); rd=(di+dj)-(di2+dj2)
            if abs(rt)>1e-15 or abs(rd)>1e-15: s.st['stale']+=1
            if s.mode=='b':
                kk=s.key(i,j); cur=s.rel.get(kk,[0.,0.]); s.rel[kk]=[cur[0]+rt,cur[1]+rd]
                s.t[i],s.d[i],s.t[j],s.d[j]=ti2,di2,tj2,dj2
            else:
                ok=True; taken=0.
                if rt<-1e-15: ok=s.take_light(i,j,0,-rt); taken=-rt if ok else 0.
                if ok and rd<-1e-15:
                    ok=s.take_light(i,j,1,-rd)
                    if not ok and taken>0: c=s.new(taken,0.); s.link(c,i); s.link(c,j)
                if not ok: s.st['void']+=1
                else:
                    s.t[i],s.d[i],s.t[j],s.d[j]=ti2,di2,tj2,dj2
                    for (a,b) in ((rt,0.),(0.,rd)):
                        if a>1e-15 or b>1e-15: c=s.new(a,b); s.link(c,i); s.link(c,j); s.st['emitted']+=a+b
            if bm: s.rec[(ii,jj)]=(tj,dj); s.rec[(jj,ii)]=(ti,di)
        else:                                               # crossover birth
            s.t[i],s.d[i],s.t[j],s.d[j]=ti/2,di/2,tj/2,dj/2
            for (a,b) in ((ti/2,dj/2),(tj/2,di/2)):
                if a>0 or b>0:
                    c=s.new(a,b); s.link(c,i); s.link(c,j)
                    if a>0 and b>0: s.st['births']+=1
            if bm: s.rec[(ii,jj)]=(tj,dj); s.rec[(jj,ii)]=(ti,di)
        s.e+=1
    def snapshot(s):
        idx=np.flatnonzero(s.alive); t=s.t[idx]; d=s.d[idx]; m=(t>0)&(d>0)
        eta=np.sqrt(t[m]*d[m]); light=(t[~m].sum()+d[~m].sum())/2
        relT=sum(v[0] for v in s.rel.values()); relD=sum(v[1] for v in s.rel.values())
        debt=sum(1 for v in s.rel.values() if v[0]<0 and v[1]<0)
        return dict(M=int(m.sum()),L=int((~m).sum()),giant=float(eta.max()/eta.sum()) if len(eta) else float('nan'),
                    light=float(light),rem=float(1-eta.sum()),relT=relT,relD=relD,nrel=len(s.rel),debt=debt,
                    tot=float(t.sum()+relT),totd=float(d.sum()+relD))
def run(mode,q,seed,E=30000,N0=200,f=0.0,every=5000,sel='pair'):
    w=World(N0,seed,mode,f); w.sel=sel; rows=[]
    for e in range(E+1):
        if e%every==0: rows.append((e,w.snapshot()))
        if e%250==0:
            M=sum(1 for k in np.flatnonzero(w.alive) if w.massive(k))
            if M<2: rows.append((e,'collapsed')); break
        if len(w.free)<200: rows.append((e,'cap')); break
        w.step(q)
    return w,rows
if __name__=="__main__":
    mode=sys.argv[1]; q=float(sys.argv[2]); f=float(sys.argv[3]); seeds=[int(x) for x in sys.argv[4].split(',')]; E=int(sys.argv[5])
    sel=sys.argv[6] if len(sys.argv)>6 else 'pair'
    for seed in seeds:
        w,rows=run(mode,q,seed,E=E,f=f,sel=sel)
        out=[]
        for e,sn in rows:
            if isinstance(sn,str): out.append(f"{sn}@{e}")
            else: out.append(f"e{e}:M={sn['M']},L={sn['L']},giant={sn['giant']:.2f},rem={sn['rem']:.3f}"+(f",light={sn['light']:.3f}" if mode=='a' else "")+(f",rel=({sn['relT']:+.4f},{sn['relD']:+.4f}),debts={sn['debt']}/{sn['nrel']}" if mode=='b' else ""))
        print(f"[{mode}/{sel} q={q} f={f} s{seed}] "+" | ".join(out)+f" || {w.st} tot=({w.snapshot()['tot']:.6f},{w.snapshot()['totd']:.6f})",flush=True)
