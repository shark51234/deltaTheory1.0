import math, random
def pair(ea,eb,p,q,K,T=400,dt=0.001):
    ta=tb=0.0; ts=[]
    for n in range(int(T/dt)):
        psi=q*ta-p*tb
        da=ea-(K/q)*math.sin(psi); db=eb+(K/p)*math.sin(psi)
        ta+=da*dt; tb+=db*dt
    return ta/T, tb/T, (q*ta-p*tb)
print("2:3 pair, eta_a=2.05 eta_b=3.0 (off exact 2:3 by a bit)")
for K in (0.5,0.1,0.05):
    wa,wb,psi=pair(2.05,3.0,2,3,K)
    dA=(wa-2.05)/2.05; dB=(wb-3.0)/3.0
    print(f" K={K}: rates a={wa:.4f} b={wb:.4f} ratio={wa/wb:.4f} (2/3={2/3:.4f}) psi_drift={psi:.2f} delta_a|b={dA:+.4f} delta_b|a={dB:+.4f} Omega={wa/2:.4f}")
print("predicted Omega=(eta_a/p+eta_b/q)/2 =",(2.05/2+3.0/3)/2, " slippage 1-(q/p)r =",1-1.5*2.05/3.0)
# circle map staircase
def rot(Om,Kc=1.0,N=3000):
    th=0.0
    for i in range(N): th=th+Om-Kc/(2*math.pi)*math.sin(2*math.pi*th)
    return th/N
steps={}
for i in range(2001):
    Om=i/2000; w=round(rot(Om),3)
    steps[w]=steps.get(w,0)+1
top=sorted(steps.items(),key=lambda x:-x[1])[:8]
print("circle map K=1 widest plateaus (ratio: share of Omega axis)")
for w,c in top: print(f"  {w}: {c/2001:.3f}")
# turnover: N members, 1:1 band, random death/rebirth
random.seed(1)
N=40; K=1.5; eta0=1.0; spread=0.3; life=20.0; dt=0.01; T=400
th=[random.uniform(0,6.28) for _ in range(N)]; et=[eta0+random.uniform(-spread,spread) for _ in range(N)]
Th=0.0; rs=[]; deaths=0
for n in range(int(T/dt)):
    cx=sum(math.cos(x) for x in th)/N; sy=sum(math.sin(x) for x in th)/N
    R=math.hypot(cx,sy); Ph=math.atan2(sy,cx)
    for i in range(N):
        th[i]+= (et[i]+K*R*math.sin(Ph-th[i]))*dt
        if random.random()<dt/life:
            th[i]=random.uniform(0,6.28); et[i]=eta0+random.uniform(-spread,spread); deaths+=1
    if n%4000==0: rs.append(round(R,2))
print(f"turnover: member lifetime {life}, run {T}, total deaths {deaths} (~{deaths/N:.0f} full replacements)")
print(" system coherence R over time:",rs)
