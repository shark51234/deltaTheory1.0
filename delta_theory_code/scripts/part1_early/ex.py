import math
# two-part universe, totals normalized: tau=delta=1, I=1
def run(x0,y0,lag,N=40,show=(0,1,2,3,4,5,10,20,39)):
    xs=[x0,x0]; ys=[y0,y0]   # history (t=-1, t=0 identical)
    for n in range(1,N+1):
        xa,ya=xs[-1],ys[-1]
        yb_seen = 1-(ys[-1-lag])     # b's difference as it arrives at a
        ya_seen = ys[-1-lag]         # a's difference as it arrives at b
        F = xa*yb_seen - (1-xa)*ya_seen
        xs.append(xa-F); ys.append(ya+F)
    out=[]
    for n in show:
        xa,ya=xs[n+1],ys[n+1]; xb,yb=1-xa,1-ya
        ok = min(xa,ya,xb,yb)>0
        ea=math.sqrt(xa*ya) if xa*ya>0 else float('nan'); eb=math.sqrt(xb*yb) if xb*yb>0 else float('nan')
        out.append(f" n={n:2d} a=({xa:.3f},{ya:.3f}) b=({xb:.3f},{yb:.3f}) eta_a={ea:.4f} eta_b={eb:.4f} sum={ea+eb:.4f} {'' if ok else 'NEGATIVE'}")
    return out
print("ELASTIC (no latency), start a=(0.7,0.2)")
print("\n".join(run(0.7,0.2,0,N=10,show=(0,1,2,3,9))))
print("\nONE-STEP LATENCY, start a=(0.7,0.2)")
print("\n".join(run(0.7,0.2,1)))
