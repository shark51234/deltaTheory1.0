import cmath, math
def run(wa,wb,ka,kb,lab,lba,N=4000,ea=0.9,eb=0.8+0.3j):
    A=[ea]; B=[eb]
    for n in range(N):
        a_in = B[max(0,n-lab)]; b_in = A[max(0,n-lba)]
        a = cmath.exp(1j*wa)*(A[n]+ka*(a_in-A[n]))
        b = cmath.exp(1j*wb)*(B[n]+kb*(b_in-B[n]))
        A.append(a); B.append(b)
    a,b=A[-1],B[-1]
    fa=cmath.phase(A[-1]/A[-2]) if abs(A[-2])>1e-300 else float('nan')
    rel=abs(a-b)/(abs(a)+abs(b)) if abs(a)+abs(b)>0 else float('nan')
    return abs(a),abs(b),abs(a-b),rel,fa
cases=[
 ("identical, no delay",      .3,.3,.2,.2,0,0),
 ("identical, delay 1",       .3,.3,.2,.2,1,1),
 ("identical, delay 3",       .3,.3,.2,.2,3,3),
 ("identical, w=0, delay 3",  0,0,.2,.2,3,3),
 ("diff w, no delay",         .3,.35,.2,.2,0,0),
 ("diff w, delay 2",          .3,.35,.2,.2,2,2),
 ("diff kappa, delay 2",      .3,.3,.1,.4,2,2),
]
print(f"{'case':26s} |ea|     |eb|     |ea-eb|   rel.diff  freq/step (w_a,w_b)")
for c in cases:
    name,wa,wb,ka,kb,l1,l2=c
    r=run(wa,wb,ka,kb,l1,l2)
    print(f"{name:26s} {r[0]:.2e} {r[1]:.2e} {r[2]:.2e} {r[3]:.3f}    {r[4]:+.4f}  ({wa},{wb})")
print()
for c in [("diff kappa, no delay",.3,.3,.1,.4,0,0),("both kappa=1, no delay",.3,.3,1,1,0,0)]:
    name,wa,wb,ka,kb,l1,l2=c
    r=run(wa,wb,ka,kb,l1,l2)
    print(f"{name:26s} {r[0]:.2e} {r[1]:.2e} {r[2]:.2e} {r[3]:.3f}    {r[4]:+.4f}")
