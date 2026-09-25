import numpy as np
from layer import *
from coupled import build
# The direct test of a circle symmetry between interacting composites.  R(alpha) turns EVERY internal wave of BOTH
# composites forward by alpha (each in its own sense).  If the interaction respects a common circle, evolving a turned
# state must give the turned evolved state.  Control: turn only A's waves (a local turn), which should matter.
def rotator(JA,alpha):
    ev,V=np.linalg.eig(JA); W=np.linalg.inv(V)
    f=np.where(ev.imag>1e-9,np.exp(1j*alpha),np.where(ev.imag<-1e-9,np.exp(-1j*alpha),1))
    return np.real(V@np.diag(f)@W)
def test(kind,N,alphas=(0.5,1.3,2.0,2.9,4.1,5.3),nmodes=5):
    n,E,JT,JA,iA,iB,pa,m=build(kind,N,pick=0)
    g=np.ones(m); g[2*n:]=0.5; gB=np.zeros(m); gB[list(range(n,2*n))]=1; gB[[2*n+E+i for i in range(E)]]=0.5
    ev,V=np.linalg.eig(JA)
    ok=[j for j in range(len(ev)) if 0.08<np.angle(ev[j])/(2*np.pi)<0.42
        and abs(V[pa,j])**2/np.sum(np.abs(V[:n,j])**2)>=0.5/n]
    ok=sorted(ok,key=lambda j:np.angle(ev[j])); pickj=[ok[int(i)] for i in np.linspace(0,len(ok)-1,min(nmodes,len(ok)))]
    RA={a:rotator(JA,a) for a in alphas}; T=max(300,20*n); res=[]
    for j in pickj:
        vA=np.zeros(m,complex); vA[iA]=V[:,j]; z0=2*np.real(vA); Q0=g@z0**2
        moved=0; dg=0; dl=0
        for a in alphas:
            Rg=np.eye(m); Rg[np.ix_(iA,iA)]=RA[a]; Rg[np.ix_(iB,iB)]=RA[a]
            Rl=np.eye(m); Rl[np.ix_(iA,iA)]=RA[a]
            z=z0.copy(); yg=Rg@z0; yl=Rl@z0
            for t in range(T):
                if t%10==0:
                    moved=max(moved,gB@z**2/Q0)
                    dg=max(dg,np.sqrt(g@(yg-Rg@z)**2/Q0)); dl=max(dl,np.sqrt(g@(yl-Rl@z)**2/Q0))
                z=JT@z; yg=JT@yg; yl=JT@yl
        res.append((moved,dg,dl))
    return n,np.median(np.array(res),0),len(pickj)
if __name__=="__main__":
    for kind,sizes in (("pair",(2,)),("triangle",(3,)),("ring",(8,16,32,64,128)),("net",(12,24,48,96,192))):
        for N in sizes:
            n,(moved,dg,dl),k=test(kind,N)
            print(f"{kind:8s} {n:3d} parts ({k} waves): energy reaching B {moved:.2f}; mismatch after a COMMON turn {dg:6.1%}; "
                  f"after turning A alone {dl:6.1%}")
