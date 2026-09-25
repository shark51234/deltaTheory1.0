import math
def h(x,w=1.0): return x*x*math.exp(-x*x/w/w)
def run(name,t,k=0.5,D=100.0,N=400000,dn=0.01,marks=(0,1000,10000,100000,399999)):
    print(name)
    for n in range(N):
        L=[math.log(v) for v in t]
        c=[sum(h(L[i]-L[j]) for j in range(3) if j!=i) for i in range(3)]
        e=[k*c[i]*(1-t[i]/D) for i in range(3)]
        t=[t[i]*math.exp(e[i]*dn) for i in range(3)]
        if n in marks:
            x=[L[0]-L[1],L[1]-L[2],L[0]-L[2]]
            print(f" n={n*dn:6.0f} t=({t[0]:6.2f},{t[1]:6.2f},{t[2]:6.2f}) xAB={x[0]:+.3f} xBC={x[1]:+.3f} xAC={x[2]:+.3f} eps=({e[0]:.4f},{e[1]:.4f},{e[2]:.4f})")
run("all inside window",[40,20,10])
run("chain: A-C out of range, B in middle",[60,8,1])
run("pair + distant third",[40,20,0.5])
# two-clock baseline for chain ends
def run2(name,t,k=0.5,D=100.0,N=400000,dn=0.01):
    for n in range(N):
        x=math.log(t[0]/t[1]); e=[k*h(x)*(1-v/D) for v in t]
        t=[t[i]*math.exp(e[i]*dn) for i in range(2)]
    print(name,[round(v,2) for v in t], round(math.log(t[0]/t[1]),3))
run2("A-C alone (baseline)",[60,1])
