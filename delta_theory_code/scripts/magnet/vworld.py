import os as _os_root
_ROOT=_os_root.path.dirname(_os_root.path.dirname(_os_root.path.abspath(__file__)))
import os
import numpy as np, random, sys
sys.path.insert(0,os.path.join(_ROOT,'binding'))
from bind import World
class V(World):
    def __init__(s,seed,mode):
        s.mode=mode; super().__init__(seed,records=True)
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
                if s.mode=='absorb':
                    s.t[dom]+=s.t[sub]; s.d[dom]+=s.d[sub]+sg
                else:
                    # vanishing as an act: continuity stays with the registering part, difference spreads to all
                    # neighbours by the Doppler rate at which each registers it (the pair's debt is settled first)
                    s.t[dom]+=s.t[sub]; D=s.d[sub]+sg
                    if D<=0: s.d[dom]+=D
                    else:
                        nbrs=list(s.nb[sub]); thg=0.5*np.log(s.t[sub]/s.d[sub])
                        w=np.array([np.exp(0.5*np.log(s.t[m]/s.d[m])-thg) for m in nbrs]); w/=w.sum()
                        for m,wm in zip(nbrs,w): s.d[m]+=D*wm
                s.sig.pop(s.key(dom,sub),None)
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
