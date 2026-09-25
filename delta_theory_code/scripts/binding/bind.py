import numpy as np, random, sys, json
class World:
    """Derived rules + records: a part builds its registration of a partner from its record of that partner
       (the partner as it was at their last contact). What the pieces claim and what the parts actually give
       differ by a residue, and the relation between them carries it (signed). Only difference is registered,
       so relation states live in the difference component."""
    def __init__(s,seed,records=True,cap=120000):
        s.r=np.random.default_rng(seed); random.seed(seed); s.records=records
        s.t=np.zeros(cap); s.d=np.zeros(cap); s.alive=np.zeros(cap,bool); s.nb=[set() for _ in range(cap)]
        s.free=list(range(cap-1,-1,-1)); s.al=[]; s.pos={}; s.e=0
        s.rec={}; s.sig={}          # rec[(i,j)] = j's difference as i last registered it; sig[(a,b)] = relation's difference state
        s.c=dict(two=0,absorb=0,cross=0,blocked=0)
        a=s.new(0.6,0.4); b=s.new(0.4,0.6); s.link(a,b)
    def new(s,t,d):
        k=s.free.pop(); s.t[k]=t; s.d[k]=d; s.alive[k]=True; s.nb[k]=set(); s.pos[k]=len(s.al); s.al.append(k); return k
    def kill(s,k):
        s.alive[k]=False; p=s.pos.pop(k); last=s.al.pop()
        if last!=k: s.al[p]=last; s.pos[last]=p
        s.free.append(k)
    @staticmethod
    def key(a,b): return (a,b) if a<b else (b,a)
    def link(s,a,b):
        if a==b or b in s.nb[a]: return
        s.nb[a].add(b); s.nb[b].add(a); s.rec[(a,b)]=s.d[b]; s.rec[(b,a)]=s.d[a]
    def seen(s,i,j):   # i's registration of j's difference
        return s.rec.get((i,j),s.d[j]) if s.records else s.d[j]
    def add_sig(s,a,b,x):
        if x!=0.0: k=s.key(a,b); s.sig[k]=s.sig.get(k,0.0)+x
    def step(s):
        i=s.al[s.r.integers(len(s.al))]; nb=list(s.nb[i])
        if not nb: s.e+=1; return
        thi=0.5*np.log(s.t[i]/s.d[i]); j=random.choices(nb,weights=[np.exp(thi-0.5*np.log(s.t[m]/s.d[m])) for m in nb])[0]
        ti,di,tj,dj=s.t[i],s.d[i],s.t[j],s.d[j]
        di_seen=s.seen(j,i); dj_seen=s.seen(i,j)
        if (ti-tj)*(di-dj)<=0:
            s.c['two']+=1
            if random.random()<di/(di+dj): act,oth,dact,doth,dact_seen,doth_seen=i,j,di,dj,di_seen,dj_seen
            else: act,oth,dact,doth,dact_seen,doth_seen=j,i,dj,di,dj_seen,di_seen
            ta,to=s.t[act],s.t[oth]
            # act keeps its row: its own half plus its registration of oth; oth halves; oth's registration of act is born
            s.t[act],s.d[act]=ta,0.5*dact+0.5*doth_seen
            s.t[oth],s.d[oth]=to/2,doth/2
            c=s.new(to/2,0.5*dact_seen)
            # residue: what the pieces claim vs what the parts actually gave
            s.add_sig(act,oth,0.5*(doth-doth_seen)+0.5*(dact-dact_seen))
            s.link(c,act); s.link(c,oth)
        else:
            dom,sub=(i,j) if ti>tj else (j,i)
            if random.random()<s.d[dom]/(s.d[dom]+s.d[sub]):
                sg=s.sig.get(s.key(dom,sub),0.0)
                if s.d[dom]+s.d[sub]+sg<=0: s.c['blocked']+=1; s.e+=1; return      # a debt the pair cannot cover forbids the merger
                s.c['absorb']+=1
                s.t[dom]+=s.t[sub]; s.d[dom]+=s.d[sub]+sg; s.sig.pop(s.key(dom,sub),None)
                for m in list(s.nb[sub]):
                    s.nb[m].discard(sub)
                    old=s.sig.pop(s.key(sub,m),0.0); r_m=s.rec.pop((m,sub),None); r_s=s.rec.pop((sub,m),None)
                    if m==dom: continue
                    if m not in s.nb[dom]:
                        s.nb[dom].add(m); s.nb[m].add(dom)
                        s.rec[(dom,m)]=r_s if r_s is not None else s.d[m]; s.rec[(m,dom)]=r_m if r_m is not None else s.d[dom]
                    if old: s.add_sig(dom,m,old)
                s.nb[sub]=set(); s.kill(sub)
            else:
                s.c['cross']+=1
                tD,dD,tS,dS=s.t[dom],s.d[dom],s.t[sub],s.d[sub]
                dS_seen=s.seen(dom,sub); dD_seen=s.seen(sub,dom)
                s.t[dom],s.d[dom],s.t[sub],s.d[sub]=tD/2,dD/2,tS/2,dS/2
                c1=s.new(tD/2,0.5*dS_seen); c2=s.new(tS/2,0.5*dD_seen)
                s.add_sig(dom,sub,0.5*(dS-dS_seen)+0.5*(dD-dD_seen))
                for c in (c1,c2): s.link(c,dom); s.link(c,sub)
        # both register each other as they were at this contact
        if s.alive[i] and s.alive[j] and j in s.nb[i]: s.rec[(i,j)]=dj; s.rec[(j,i)]=di
        s.e+=1
    def binding(s):
        eta=lambda k: np.sqrt(s.t[k]*s.d[k])
        B=[]; bound=0; n=0; debts=0; tot_sig=0.0
        for (a,b),sg in s.sig.items():
            if not (s.alive[a] and s.alive[b]): continue
            n+=1; tot_sig+=sg; debts+= sg<0
            T=s.t[a]+s.t[b]; D=s.d[a]+s.d[b]+sg
            ec=np.sqrt(T*D) if D>0 else 0.0; free=eta(a)+eta(b)
            B.append((free-ec)/free)
            if ec<free: bound+=1
        ne=sum(len(s.nb[k]) for k in s.al)//2
        return dict(N=len(s.al),relations=ne,with_state=n,bound=bound,debts=debts,
                    medB=float(np.median([b for b in B if b>0])) if any(b>0 for b in B) else 0.0,
                    totsig=tot_sig,sumd=float(s.d[s.al].sum()),sumt=float(s.t[s.al].sum()))
if __name__=="__main__":
    seed=int(sys.argv[1]); rec=sys.argv[2]=='rec'; marks=[int(x) for x in sys.argv[3].split(',')]
    w=World(seed,records=rec); mk=list(marks)
    while mk:
        if len(w.al)<2: print(f"seed {seed}: collapsed at {w.e}"); break
        if len(w.al)>=mk[0]:
            b=w.binding(); mk.pop(0)
            print(f"seed {seed} {'records' if rec else 'no records'}: N={b['N']} relations={b['relations']} | carrying a state {b['with_state']} "
                  f"(debts {b['debts']}) | bound pairs {b['bound']} ({b['bound']/max(b['relations'],1):.1%} of relations), median binding {b['medB']:.1%} of the pair's free mass | "
                  f"blocked mergers {w.c['blocked']} | conservation: sum(tau)={b['sumt']:.6f}, sum(delta)+relations={b['sumd']+b['totsig']:.6f}",flush=True)
        w.step()
