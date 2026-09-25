import math
def run(ta,tb,k=0.5,w=1.0,D=100.0,N=200000,dn=0.01):
    for n in range(N):
        x=math.log(ta/tb); h=x*x*math.exp(-x*x/w/w)
        ea=k*h*(1-ta/D); eb=k*h*(1-tb/D)
        ta*=math.exp(ea*dn); tb*=math.exp(eb*dn)
        if n in (0,1000,10000,50000,199999):
            print(f"n={n*dn:8.0f} ta={ta:7.3f} tb={tb:7.3f} x={x:+.4f} eps_a={ea:.5f}")
print("inside window"); run(40,10)
print("outside window"); run(90,2)
print("no Delta"); run(40,10,D=1e12)
