import numpy as np
cimport numpy as np 

cdef double median(double[:, :] l1): # reduce this to not use sum and len/sort.
        cdef double[:] ls = sum(l1,[])
        n = len(ls)
        ls.sort()
        cdef int id = n//2
        if n % 2 == 0:
            return (ls[id] + ls[id - 1])/2
        else:
            return ls[id]

cdef double[:,:] zeros(int n, int m):
    cdef double[:,:] z
    cdef int i = 0, j = 0
    while i < n:
        while j < m:
            z[i][j] = 0.0
            j += 1
        i += 1
    return z
    

def medianfilter(double[:,:] r, double[:,:] g, double[:,:] b, double[:] args):
    cdef int l1 = len(r)
    cdef int l2 = len(r[0])
    cdef double[:,:] zr = zeros(l1,l2)
    cdef double [:, :] new_r = zr
    cdef double [:, :] new_g = zr
    cdef double [:, :] new_b = zr
    
    if args[0] == 1 and args[1] == 1:
        return r,g,b

    cdef int x = int(args[0]/2)
    cdef int y = int(args[1]/2)
    cdef unsigned long i = y,j = x

    while i < len(r)-1-y:
        while j < len(r[0])-1-x:
            
            new_r[i,j] = median(r[i-y:i+y,j-x:j+x])
            new_g[i,j] = median(g[i-y:i+y,j-x:j+x])
            new_b[i,j] = median(b[i-y:i+y,j-x:j+x])
            j += 1
        j = x
        i += 1
    return new_r, new_g, new_b