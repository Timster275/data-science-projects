cdef double[:,:] smooth(double[:,:] inp):
    for i in range(len(inp)):
        for j in range(len(inp[0])):
            if inp[i,j] > 255:
                inp[i,j] = 255
            elif inp[i,j] < 0:
                inp[i,j] = 0 
    return inp