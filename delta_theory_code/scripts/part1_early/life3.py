import math, random, bisect
def sim(parts0,q,E,seed,cap=20000,every=10000):
    random.seed(seed); P=[p[:] for p in parts0]; nid=len(P); out=[]
    for e in range(E+1):
        if e%every==0: out.append((e,len(P),sum(math.sqrt(t*d) for t,d,_,_ in P)))
        if len(P)<2: out.append(('collapsed',e)); break
        if len(P)>cap: out.append(('exceeded cap',e)); break
        ct=[];s=0
        for p in P: s+=p[0]; ct.append(s)
        cd=[];s2=0
        for p in P: s2+=p[1]; cd.append(s2)
        while True:
            i=min(bisect.bisect_left(ct,random.random()*s),len(P)-1); j=min(bisect.bisect_left(cd,random.random()*s2),len(P)-1)
            if i!=j: break
        ta,da,_,_=P[i]; tb,db,_,_=P[j]
        w=[ta*da,tb*db,ta*db,tb*da]; r=random.random()*sum(w); k=0; acc=w[0]
        while r>acc: k+=1; acc+=w[k]
        if k<2:
            if random.random()<q:
                keep,gone=(i,j) if k==0 else (j,i)
                P[keep][0]+=P[gone][0]; P[keep][1]+=P[gone][1]; P.pop(gone)
            else:
                T=ta+tb; D=da+db
                P[i][0],P[i][1]=T*da/D,D*ta/T; P[j][0],P[j][1]=T*db/D,D*tb/T
        else:
            P[i][0],P[i][1]=ta/2,da/2; P[j][0],P[j][1]=tb/2,db/2
            P.append([ta/2,db/2,nid,e]); P.append([tb/2,da/2,nid+1,e]); nid+=2
    return out
random.seed(9); r=[[random.uniform(.2,1.8),random.uniform(.2,1.8)] for _ in range(20)]
T=sum(x[0] for x in r); D=sum(x[1] for x in r); s20=[[x[0]/T,x[1]/D,k,0] for k,x in enumerate(r)]
for q in (0.5,0.75,0.9):
    for seed in (1,2):
        o=sim(s20,q,60000,seed)
        print(f"q={q} seed={seed}: "+"; ".join(f"{x[0]}:{x[1]}" if isinstance(x[0],str) else f"e{x[0]}:N={x[1]}" for x in o))
