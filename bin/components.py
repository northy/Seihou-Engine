import numpy as np

def truncate(a,b) :
    if np.linalg.norm(a)>b :
        a/=np.linalg.norm(a)
        a*=b
    return a