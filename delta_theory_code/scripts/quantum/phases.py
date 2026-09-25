import numpy as np
# Two parts, totals normalized (tau = delta = 1). Part a has shares (x, y); b has (1-x, 1-y).
# Exchange law in flux form, with registration of difference arriving after a latency of l ticks
# (continuity is each part's own and current; only difference propagates, Ch. 8; Ch. 5 forbids l = 0):
#   F = x(n)(1 - y(n-l)) - (1 - x(n)) y(n-l) = x(n) - y(n-l)
#   x(n+1) = x(n) - F = y(n-l),   y(n+1) = y(n) + F = y(n) + x(n) - y(n-l)
# Hence y(n+1) = y(n) - y(n-l) + y(n-l-1): characteristic (lam-1)(lam^(l+1)+1) = 0.
for l in range(0,5):
    c=np.zeros(l+3); c[0]=1; c[1]=-1; c[l+1]+=1; c[l+2]+=-1     # lam^(l+2) - lam^(l+1) + lam - 1
    roots=np.roots(c)
    mods=np.abs(roots); angs=np.sort(np.round(np.abs(np.angle(roots))/np.pi,4))
    print(f"latency {l}: |roots| = {np.round(np.sort(mods),6).tolist()}  |angle|/pi = {angs.tolist()}  predicted odd multiples of 1/{l+1}")
# simulate and measure: frequency content and whether the oscillation grows or decays
print()
for l in (1,2,3):
    N=4096; y=[0.5]*(l+2); x=[0.5]*(l+2)
    y[-1]=0.53; x[-1]=0.47            # a small initial imbalance
    for n in range(N):
        yn=y[-1]+x[-1]-y[-1-l]; xn=y[-1-l]
        x.append(xn); y.append(yn)
    y=np.array(y[l+2:]); x=np.array(x[l+2:])
    s=y-y.mean(); spec=np.abs(np.fft.rfft(s)); f=np.fft.rfftfreq(len(s))
    peaks=f[np.argsort(spec)[-3:]]
    first=np.abs(s[:200]).max(); last=np.abs(s[-200:]).max()
    print(f"latency {l}: strongest frequencies (cycles/tick) {np.round(np.sort(peaks),4).tolist()}, predicted {[round((2*m+1)/(2*(l+1)),4) for m in range((l+2)//2)]}; "
          f"oscillation size first/last {first:.4f}/{last:.4f}; shares stay in (0,1): {bool((x>0).all() and (x<1).all() and (y>0).all() and (y<1).all())}")
