import math, random, statistics as st
def init(N,seed):
    random.seed(seed)
    t=[random.uniform(0.2,1.8) for _ in range(N)]; d=[random.uniform(0.2,1.8) for _ in range(N)]
    T=sum(t); D=sum(d); return [v/T for v in t],[v/D for v in d]
def rnd_round(t,d,weighted):
    N=len(t); idx=list(range(N)); random.shuffle(idx)
    if weighted:  # pair partners with prob ~ mutual registration t_a d_b + t_b d_a (greedy)
        pairs=[]; free=set(idx)
        for a in idx:
            if a not in free: continue
            free.discard(a); cand=list(free)
            if not cand: break
            w=[t[a]*d[b]+t[b]*d[a] for b in cand]
            b=random.choices(cand,weights=w)[0]; free.discard(b); pairs.append((a,b))
    else:
        pairs=[(idx[k],idx[k+1]) for k in range(0,N-1,2)]
    for a,b in pairs:   # elastic exchange: each part's shares of the pair totals swap
        T=t[a]+t[b]; D=d[a]+d[b]
        ta,da,tb,db=t[a],d[a],t[b],d[b]
        t[a],d[a]=T*da/D, D*ta/T
        t[b],d[b]=T*db/D, D*tb/T
def run(weighted,N=60,R=20000,seed=5):
    t,d=init(N,seed)
    m=[math.sqrt(a*b) for a,b in zip(t,d)]
    acc=[0.0]*N; cnt=0
    for r in range(R):
        rnd_round(t,d,weighted)
        if r>R//2:
            for i in range(N):
                E=(t[i]+d[i])/2; p=(t[i]-d[i])/2
                acc[i]+=p*p/E
            cnt+=1
    pv=[a/cnt for a in acc]
    order=sorted(range(N),key=lambda i:m[i])
    lo=[pv[i] for i in order[:N//3]]; hi=[pv[i] for i in order[-N//3:]]
    KE=1-sum(m)
    print(f"{'weighted' if weighted else 'uniform '} pairing: sum of masses={sum(m):.4f}, kinetic remainder={KE:.4f}")
    print(f"   <p v> lightest third={st.mean(lo):.5f}  heaviest third={st.mean(hi):.5f}  all: mean={st.mean(pv):.5f} sd={st.pstdev(pv):.5f}")
    print(f"   masses range {min(m):.4f}-{max(m):.4f};  2*remainder/N={2*KE/N:.5f}")
    # rapidity spread by mass
    th=[0.5*math.log(t[i]/d[i]) for i in range(N)]
    print(f"   final |rapidity| light third={st.mean(abs(th[i]) for i in order[:N//3]):.3f}, heavy third={st.mean(abs(th[i]) for i in order[-N//3:]):.3f}")
run(False); run(True)
