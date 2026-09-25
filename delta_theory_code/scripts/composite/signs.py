import numpy as np
from layer import *
from coupled import build
from circle_local import local_commutant
# (1) Can the joining relation compensate a turn of A alone?  Search every linear transformation acting on A's
#     members, A's relations and the joining relation's memory that leaves a round of the joined system unchanged.
for kind,N in (("pair",2),("triangle",3),("ring",8),("net",12)):
    n,E,JT,JA,iA,iB,pa,m=build(kind,N,pick=0)
    S=iA+[m-1]; basis=local_commutant(JT,S)
    rng=np.random.default_rng(1); rotlike=0
    for _ in range(500):
        if not basis: break
        M=sum(rng.normal()*B for B in basis); rotlike+=np.abs(np.linalg.eigvals(M).imag).max()>1e-8
    print(f"joined {kind}s: transformations of A plus the joining relation that commute with a round: {len(basis)}; rotation-like: {rotlike}")
# (2) Two senses.  In a ring, waves come in degenerate pairs; sort them by circulation using the ring's own shift
#     symmetry (move every member two places on), check that mirror reflection swaps the senses, then send a
#     wave of one sense from A and see which sense arrives in B.
def shift2(n,E):
    m=n+E; S=np.zeros((m,m))
    for j in range(n): S[(j+2)%n,j]=1
    for k in range(E): S[n+(k+2)%E,n+k]=1
    return S
def mirror(n,E):
    m=n+E; P=np.zeros((m,m))
    for j in range(n): P[(1-j)%n,j]=1
    for k in range(E): P[n+(-k)%E,n+k]=-1                     # the relation is traversed the other way round
    return P
for N in (16,32,64):
    n,E,JT,JA,iA,iB,pa,m=build("ring",N,pick=0)
    S=shift2(n,E); P=mirror(n,E)
    print(f"ring of {n}: shift commutes with a round {np.abs(S@JA-JA@S).max():.0e}; mirror commutes {np.abs(P@JA-JA@P).max():.0e}")
    ev,V=np.linalg.eig(JA); g=np.ones(m); g[2*n:]=0.5; gl=np.ones(n+E); gl[n:]=0.5
    rates=sorted(set(np.round(np.angle(ev[ev.imag>1e-9])/(2*np.pi),6)))
    for rate in [r for r in rates if 0.12<r<0.38][::3][:3]:
        idx=[k for k in range(len(ev)) if abs(np.angle(ev[k])/(2*np.pi)-rate)<1e-5]
        if len(idx)!=2: continue
        Vd=V[:,idx]; Sd=np.linalg.pinv(Vd)@S@Vd; sv,su=np.linalg.eig(Sd); U=Vd@su     # circulation-sorted waves
        order=np.argsort(np.angle(sv)); U=U[:,order]; sv=sv[order]
        Vfull=V.copy(); Vfull[:,idx]=U; Wfull=np.linalg.inv(Vfull)
        swap=abs(Wfull[idx[1]]@(P@U[:,0]))/np.linalg.norm(Wfull[idx]@(P@U[:,0]))
        vA=np.zeros(m,complex); vA[iA]=U[:,0]; z=2*np.real(vA); Q0=g@z**2; same=opp=0; best=0
        for t in range(40*n):
            cB=Wfull[idx]@z[iB]
            eB=[gl@(2*np.real(U[:,k]*cB[k]))**2/Q0 for k in (0,1)]
            if sum(eB)>best: best=sum(eB); same,opp=eB
            z=JT@z
        print(f"   waves at {rate:.3f} turns/round: mirror image of one sense lies in the other sense {swap:.0%}; "
              f"at peak transfer B holds {best:.2f} of the energy, {opp/(same+opp):.0%} of it in the OPPOSITE sense")
