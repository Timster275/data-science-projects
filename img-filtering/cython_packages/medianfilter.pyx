import numpy as np
cimport numpy as np 

DTYPE = np.float
ctypedef np.float_t DTYPE_t

def medianfilter(np.ndarray[DTYPE_t, ndim=2] r,np.ndarray[DTYPE_t, ndim=2] g, np.ndarray[DTYPE_t, ndim=2]b, kwargs):
    new_r = np.zeros((len(r),len(r[0])))
    new_g = np.zeros((len(r),len(r[0])))
    new_b = np.zeros((len(r),len(r[0])))
    
    if kwargs[0] == 1 and kwargs[1] == 1:
        return r,g,b
    if kwargs[0] ==1 :
        kwargs[0] = 2
    if kwargs[1] ==1 :
        kwargs[1] = 2

    cdef int x = int(kwargs[0])//2
    cdef int y = int(kwargs[1])//2
    
    print(r[0][0:10])
    for i in range(y, len(r)-1-y):
        for j in range(x, len(r[i])-1-x):
            new_r[i][j] = np.median(r[i-y:i+y,j-x:j+x])
            new_g[i][j] = np.median(g[i-y:i+y,j-x:j+x])
            new_b[i][j] = np.median(b[i-y:i+y,j-x:j+x])
    return new_r, new_g, new_b