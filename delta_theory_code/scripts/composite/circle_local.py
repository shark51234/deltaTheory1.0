import numpy as np
def local_commutant(J,S):
    m=J.shape[0]; cols=[]
    for i in S:
        for j in S:
            M=np.zeros((m,m)); M[:,j]+=J[:,i]; M[i,:]-=J[j,:]; cols.append(M.ravel())
    A=np.array(cols).T; u,s,vt=np.linalg.svd(A,full_matrices=False); null=vt[s<1e-8*s[0]]
    out=[]
    for v in null:
        M=np.zeros((m,m)); M[np.ix_(S,S)]=v.reshape(len(S),len(S)); out.append(M)
    return out
