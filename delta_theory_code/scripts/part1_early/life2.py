import math, random, statistics as st, bisect
def sim(parts0, E, seed, cap=30000, every=None):
    random.seed(seed)
    P=[p[:] for p in parts0]; nid=len(P)
    births=deaths=0; lifetimes=[]; hist=[]
    for e in range(E+1):
        if every and e%every==0:
            eta=[math.sqrt(t*d) for t,d,_,_ in P]
            hist.append((e,len(P),sum(eta),births,deaths))
        if len(P)<2: hist.append(('collapsed to one part at event',e)); break
        if len(P)>cap: hist.append(('exceeded cap at event',e)); break
        # fast weighted choice via cumulative sums
        ct=[];s=0
        for p in P: s+=p[0]; ct.append(s)
        cd=[];s2=0
        for p in P: s2+=p[1]; cd.append(s2)
        while True:
            i=bisect.bisect_left(ct,random.random()*s); j=bisect.bisect_left(cd,random.random()*s2)
            i=min(i,len(P)-1); j=min(j,len(P)-1)
            if i!=j: break
        ta,da,ia,ba=P[i]; tb,db,ib,bb=P[j]
        w=[ta*da, tb*db, ta*db, tb*da]; r=random.random()*sum(w)
        k=0; acc=w[0]
        while r>acc: k+=1; acc+=w[k]
        if k<2:   # a self acts: it absorbs the other
            keep,gone=(i,j) if k==0 else (j,i)
            P[keep][0]+=P[gone][0]; P[keep][1]+=P[gone][1]
            lifetimes.append(e-P[gone][3]); P.pop(gone); deaths+=1
        else:     # the relation acts: crossover birth
            P[i][0],P[i][1]=ta/2,da/2; P[j][0],P[j][1]=tb/2,db/2
            P.append([ta/2,db/2,nid,e]); P.append([tb/2,da/2,nid+1,e]); nid+=2; births+=2
    return hist,lifetimes,P
random.seed(9); r=[[random.uniform(.2,1.8),random.uniform(.2,1.8)] for _ in range(20)]
T=sum(x[0] for x in r); D=sum(x[1] for x in r); start20=[[x[0]/T,x[1]/D,k,0] for k,x in enumerate(r)]
for seed in (1,2,3):
    hist,lt,P=sim(start20,60000,seed,every=5000)
    print(f"R1 seed {seed}:")
    for h in hist: print("  ",h if isinstance(h[0],str) else f"event {h[0]:6d} parts={h[1]:6d} sum_eta={h[2]:.4f} births={h[3]} deaths={h[4]}")
