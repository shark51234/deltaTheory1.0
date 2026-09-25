import sys, random
from polarity import V
mode=sys.argv[1]; ok=[]
for seed in range(1,120):
    random.seed(seed); w=V(seed,mode)
    while 2<=len(w.al)<400: w.step()
    if len(w.al)>=400: ok.append(seed)
    if len(ok)>=4: break
print(mode,"surviving seeds:",ok)
