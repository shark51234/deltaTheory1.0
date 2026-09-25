import numpy as np
from layer import *
from coupled import build
# Measure with the exactly conserved total Q = sum(theta^2) + 1/2 sum(r^2) (checked below), so nothing depends on
# how modes are normalised.  Composites: rings (their internal waves spread evenly over all members).
def Qform(n,E,m,idx_parts,idx_rel):
    g=np.zeros(m); g[idx_parts]=1; g[idx_rel]=0.5; return g
alphas=np.linspace(0,2*np.pi,12,endpoint=False)
for kind,sizes in (("ring",(4,8,16,32,64)),("net",(12,24,48,96))):
    for N in sizes:
        n,E,JT,JA,iA,iB,pa,m=build(kind,N,pick=0)
        g=np.ones(m); g[2*n:]=0.5
        assert np.abs(JT.T@np.diag(g)@JT-np.diag(g)).max()<1e-12      # Q is exactly conserved
        gB=np.zeros(m); gB[list(range(n,2*n))]=1; gB[[2*n+E+i for i in range(E)]]=0.5
        ev,V=np.linalg.eig(JA); W=np.linalg.inv(V)
        rot=[j for j in range(len(ev)) if ev[j].imag>1e-9]
        # a typical internal wave: median weight on the joining member
        wts=[abs(V[pa,j])**2/np.sum(np.abs(V[:n,j])**2) for j in rot]; j=rot[int(np.argsort(wts)[len(wts)//2])]
        phi=np.angle(ev[j]); band=[k for k in range(len(ev)) if abs(abs(np.angle(ev[k]))-abs(phi))<0.02]
        T=max(400,30*n); EB=[]; inband=[]
        for a in alphas:
            vA=np.zeros(m,complex); vA[iA]=V[:,j]; z=2*np.real(np.exp(1j*a)*vA); Q0=g@z**2; rowB=[]; rowK=[]
            for t in range(T):
                rowB.append(gB@z**2/Q0)
                if t%10==0:   # energy still in waves of the same rate, in A and in B
                    s=0
                    for idx in (iA,iB):
                        c=W@z[idx]; zz=np.zeros(m); zz[idx]=2*np.real(V[:,band]@c[band])
                        s+=g@zz**2
                    rowK.append(s/Q0)
                z=JT@z
            EB.append(rowB); inband.append(rowK)
        EB=np.array(EB); inband=np.array(inband)
        print(f"{kind} of {n:3d} parts: most energy ever in B {EB.max():.2f}; dependence on the common phase "
              f"{(EB.max(0)-EB.min(0)).max()/EB.max():6.1%}; energy leaving waves of that rate {1-inband.min():6.1%} (over {T} rounds)")
