import json, numpy as np
from collections import defaultdict
agg=defaultdict(list); tr=defaultdict(list); share=defaultdict(int); total=0
for s in (1,2,3):
    D=json.load(open(f"ch_{s}.json"))
    for r in D['recs']:
        key=(r['chan'],r['out']); agg[key].append(r); share[r['chan']]+=1; total+=1
    for t in D['done']: tr[(t['chan'],t['out'])].append(t)
print(f"{total} encounters over 3 seeds")
for ch in sorted(share): print(f"  {ch}: {share[ch]/total:.1%} of encounters")
print()
print(f"{'channel / outcome':52s} {'share':>6s} {'mass ang':>9s} {'motion ang':>10s} {'d(mass)':>9s} {'rel.inherit':>11s} {'max deg':>8s}")
for key in sorted(agg):
    rs=agg[key]; n=len(rs)
    print(f"{key[0]+' / '+key[1]:52s} {n/total:6.1%} {np.median([r['mass'] for r in rs]):9.2f} {np.median([r['motion'] for r in rs]):10.2f} "
          f"{np.mean([r['dmass'] for r in rs]):+9.3f} {np.mean([r['inherited'] for r in rs]):11.2f} {np.median([r['degmax'] for r in rs]):8.0f}")
print()
print(f"{'tracers started at':52s} {'n':>5s} {'reach (mean dist)':>18s} {'farthest':>9s} {'parts reached':>14s}")
for key in sorted(tr):
    ts=tr[key]
    print(f"{key[0]+' / '+key[1]:52s} {len(ts):5d} {np.mean([t['reach'] for t in ts]):18.2f} {np.mean([t['far'] for t in ts]):9.2f} {np.mean([t['count'] for t in ts]):14.1f}")
# bootstrap-ish: standard error of reach per group
print()
for key in sorted(tr):
    v=np.array([t['reach'] for t in tr[key]]); print(f"  reach {key[1]:16s}: mean {v.mean():.2f} +/- {v.std()/np.sqrt(len(v)):.2f} (s.e.)")
