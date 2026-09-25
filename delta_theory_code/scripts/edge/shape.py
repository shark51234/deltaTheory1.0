import numpy as np, json
from spectrum import loghist
D=json.load(open("spectra.json"))
def local_slopes(eta, nb=24):
    c,dens,h=loghist(np.array(eta),nb)
    med=np.median(eta); x=np.log10(c/med); y=np.log10(np.where(dens>0,dens,np.nan))
    ok=(h>=5)
    rows=[]
    for k in range(len(c)):
        if ok[k]: rows.append((x[k],y[k],h[k]))
    return rows
for key in ("0.83_7","0.83_8","0.7_7","0.5_7","0.0_7"):
    eta=np.array(D[key]["eta"]); rows=local_slopes(eta)
    xs=np.array([r[0] for r in rows]); ys=np.array([r[1] for r in rows])
    # slopes over successive half-decade windows above the median
    out=[]
    for lo in np.arange(0.25,3.25,0.5):
        m=(xs>=lo)&(xs<lo+0.75)
        if m.sum()>=3: out.append(f"[{lo:.2f},{lo+0.75:.2f}]:{np.polyfit(xs[m],ys[m],1)[0]:.2f}")
    print(f"{key}: local slopes by log10(eta/median) window: "+"  ".join(out))
