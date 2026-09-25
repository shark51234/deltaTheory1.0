import numpy as np
from covariant import colour, network
src=open('circle.py').read().split("for seed,N in")[0]; exec(src)
# The one transformation confined to part k: what does it act on and preserve?  Test the guess
#   neutral direction v_k : part k grows (ln tau_k = ln delta_k = +1) and its relations remember it grew (shares +/- 1/4)
#   conserved quantity  w_k : (ln tau_k + ln delta_k)/2 + sum over its relations of the size-share it is remembered to hold
for seed,N in ((3,12),(5,20),(11,16)):
    edges,n=network(seed,N); col,C=colour(edges); E=len(edges); J=roundmap(edges,n,col,C); worst_v=worst_w=0
    for k in range(n):
        v=np.zeros(2*n+2*E); w=np.zeros(2*n+2*E); v[k]=v[n+k]=1; w[k]=w[n+k]=0.5
        for e,(a,b) in enumerate(edges):
            if k in (a,b):
                s=1 if a==k else -1                          # the remembered split is the FIRST part's share
                v[2*n+e]=v[2*n+E+e]=s*0.25; w[2*n+e]=w[2*n+E+e]=s*1.0
        worst_v=max(worst_v,np.abs(J@v-v).max()); worst_w=max(worst_w,np.abs(w@J-w).max())
    print(f"{n} parts: every part's neutral direction unchanged by a round to {worst_v:.1e}; every part's local total conserved to {worst_w:.1e}")
