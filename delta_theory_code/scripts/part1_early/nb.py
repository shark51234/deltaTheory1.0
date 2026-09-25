import math, random, statistics as st
def init(N,seed):
    random.seed(seed)
    t=[random.uniform(0.2,1.8) for _ in range(N)]; d=[random.uniform(0.2,1.8) for _ in range(N)]
    T=sum(t); D=sum(d); return [v/T for v in t],[v/D for v in d]
def eta(t,d): return [math.sqrt(a*b) if a>0 and b>0 else float('nan') for a,b in zip(t,d)]
def rap(t,d,T,D):  # rapidity relative to the whole
    return [0.5*math.log((a/T)/(b/D)) for a,b in zip(t,d)]
def step(t,d,dprev,lag):
    N=len(t); idx=list(range(N)); random.shuffle(idx)
    nt,nd=t[:],d[:]
    for k in range(0,N-1,2):
        a,b=idx[k],idx[k+1]
        ta,tb=t[a],t[b]
        db_seen = dprev[b] if lag else d[b]
        da_seen = dprev[a] if lag else d[a]
        F = ta*db_seen - tb*da_seen
        Tab=ta+tb; Dab=d[a]+d[b]
        nd[a]=d[a]+F/Tab; nd[b]=d[b]-F/Tab
        nt[a]=ta-F/Dab;  nt[b]=tb+F/Dab
    return nt,nd
def run(lag,N=60,R=3000,seed=3):
    t,d=init(N,seed); dprev=d[:]
    e0=eta(t,d); T=sum(t); D=sum(d)
    print(f"{'LATENCY' if lag else 'ELASTIC'}: N={N}, rounds={R}")
    for r in range(R+1):
        if r in (0,10,100,1000,R):
            e=eta(t,d); th=rap(t,d,sum(t),sum(d)) if all(v>0 for v in t+d) else None
            neg=sum(1 for v in t+d if v<=0)
            drift=max(abs(x-y) for x,y in zip(e,e0)) if not any(math.isnan(x) for x in e) else float('nan')
            s=sum(e) if not any(math.isnan(x) for x in e) else float('nan')
            spread = st.pstdev(th) if th else float('nan')
            print(f"  r={r:5d} sum_eta={s:.4f} max|eta change|={drift:.4f} rapidity spread={spread:.3f} negatives={neg}  totals=({sum(t):.4f},{sum(d):.4f})")
        nt,nd=step(t,d,dprev,lag); dprev=d; t,d=nt,nd
    return t,d
tE,dE=run(0)
print()
tL,dL=run(1)
