import math, random, statistics as st
# parts: [tau, delta, id, birth_event]; totals normalized so tau=delta=1, I=1, eta=sqrt(tau*delta)
def sim(rule, parts0, E=200000, seed=1, cap=4000, report=(0,1000,10000,50000,100000,200000)):
    random.seed(seed)
    P=[p[:] for p in parts0]; nid=len(P)
    births=deaths=0; lifetimes=[]
    out=[]
    for e in range(E+1):
        if e in report:
            eta=[math.sqrt(t*d) for t,d,_,_ in P]
            out.append((e,len(P),sum(eta),1-sum(eta),births,deaths,max(eta),st.median(eta)))
        if len(P)<2 or len(P)>cap: break
        # choose ordered pair: i ~ tau, j ~ delta, i != j  -> unordered weight tau_i d_j + tau_j d_i
        while True:
            i=random.choices(range(len(P)),weights=[p[0] for p in P])[0]
            j=random.choices(range(len(P)),weights=[p[1] for p in P])[0]
            if i!=j: break
        ta,da,ia,ba=P[i]; tb,db,ib,bb=P[j]
        entries=[ta*da, tb*db, ta*db, tb*da]   # self_a, self_b, cross_ab, cross_ba
        k=random.choices(range(4),weights=entries)[0]
        self_pick = k<2
        if rule=='bounce' or (rule=='R2' and self_pick) or (rule=='R3' and not self_pick):
            T=ta+tb; D=da+db
            P[i][0],P[i][1]=T*da/D, D*ta/T
            P[j][0],P[j][1]=T*db/D, D*tb/T
        elif (rule in ('R1','R3')) and self_pick:
            keep,gone=(i,j) if k==0 else (j,i)
            P[keep][0]+=P[gone][0]; P[keep][1]+=P[gone][1]
            lifetimes.append(e-P[gone][3]); P.pop(gone); deaths+=1
        else:   # crossover birth: parents keep half; halves cross over into two children
            P[i][0],P[i][1]=ta/2,da/2
            P[j][0],P[j][1]=tb/2,db/2
            P.append([ta/2,db/2,nid,e]); P.append([tb/2,da/2,nid+1,e]); nid+=2; births+=2
    return out,lifetimes
start2=[[0.6,0.4,0,0],[0.4,0.6,1,0]]      # the first asymmetry: two parts, slight imbalance
random.seed(9); r=[[random.uniform(.2,1.8),random.uniform(.2,1.8)] for _ in range(20)]
T=sum(x[0] for x in r); D=sum(x[1] for x in r); start20=[[x[0]/T,x[1]/D,k,0] for k,x in enumerate(r)]
for rule in ('R1','R2','R3'):
    for name,s in (('2-part start',start2),('20-part start',start20)):
        out,lt=sim(rule,s)
        print(f"{rule} {name}:")
        for e,N,se,rem,b,dth,mx,md in out:
            print(f"   event {e:6d}: parts={N:5d} sum_eta={se:.4f} remainder={rem:.4f} births={b} deaths={dth} max_eta={mx:.4f} median_eta={md:.5f}")
        if lt: print(f"   lifetimes: n={len(lt)} median={st.median(lt):.0f} mean={st.mean(lt):.0f}")
