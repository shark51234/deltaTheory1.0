import numpy as np
from layer import *
from coupled import build
alphas=np.linspace(0,2*np.pi,12,endpoint=False)
def experiment(kind,N,target=0.25,T=None):
    n,E,JT,JA,iA,iB,pa,m=build(kind,N,pick=0)
    g=np.ones(m); g[2*n:]=0.5
    gB=np.zeros(m); gB[list(range(n,2*n))]=1; gB[[2*n+E+i for i in range(E)]]=0.5
    ev,V=np.linalg.eig(JA); W=np.linalg.inv(V)
    rot=[j for j in range(len(ev)) if ev[j].imag>1e-9]
    j=min(rot,key=lambda j:abs(np.angle(ev[j])/(2*np.pi)-target)); phi=np.angle(ev[j])
    band=[k for k in range(len(ev)) if abs(abs(np.angle(ev[k]))-abs(phi))<0.03]   # both senses of rotation included once each
    T=T or max(400,30*n); EB=[]; inb=[]
    for a in alphas:
        vA=np.zeros(m,complex); vA[iA]=V[:,j]; z=2*np.real(np.exp(1j*a)*vA); Q0=g@z**2; rb=[]; rk=[]
        for t in range(T):
            rb.append(gB@z**2/Q0)
            if t%10==0:
                s=0
                for idx in (iA,iB):
                    c=W@z[idx]; zz=np.zeros(m); zz[idx]=np.real(V[:,band]@c[band]); s+=g@zz**2
                rk.append(s/Q0)
            z=JT@z
        EB.append(rb); inb.append(rk)
    EB=np.array(EB); inb=np.array(inb)
    return n,phi/(2*np.pi),EB.max(),(EB.max(0)-EB.min(0)).max()/EB.max(),1-inb.min(),T
if __name__=="__main__":
    for kind,sizes in (("ring",(4,8,16,32,64,128)),("net",(12,24,48,96,192))):
        for N in sizes:
            n,rate,moved,dep,leak,T=experiment(kind,N)
            print(f"{kind} of {n:3d} parts, internal wave at {rate:.3f} turns/round: most energy ever in B {moved:.2f}; "
                  f"dependence on the common phase {dep:6.2%}; energy leaving waves of that rate {leak:6.2%}  ({T} rounds)")
