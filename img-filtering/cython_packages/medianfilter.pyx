import numpy as np
cimport numpy as np 

DTYPE = np.int
ctypedef np.int_t DTYPE_t

def medianfilter(double[:,:] r, double[:,:] g, double[:,:] b, args):
    cdef double [:, :] new_r = np.zeros((len(r),len(r[0])))
    cdef double [:, :] new_g = np.zeros((len(r),len(r[0])))
    cdef double [:, :] new_b = np.zeros((len(r),len(r[0])))
    
    
    if args[0] == 1 and args[1] == 1:
        return r,g,b
    if args[0] ==1 :
        args[0] = 2
    if args[1] ==1 :
        args[1] = 2

    cdef int x = int(args[0])//2
    cdef int y = int(args[1])//2

    cdef int i,j
    i = y
    j = x

    
    while i < len(r)-1-y:
        while j < len(r[0])-1-x:
            new_r[i][j] = np.median(r[i-y:i+y,j-x:j+x])
            new_g[i][j] = np.median(g[i-y:i+y,j-x:j+x])
            new_b[i][j] = np.median(b[i-y:i+y,j-x:j+x])
            j += 1
        j = x
        i += 1
    return new_r, new_g, new_b