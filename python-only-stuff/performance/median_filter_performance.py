import numpy as np 
from numba import jit, njit, prange, float32
import time
import timeit
def medianfilter(r,g,b, kwargs):
    new_r = np.zeros((len(r),len(r[0])))
    new_g = np.zeros((len(r),len(r[0])))
    new_b = np.zeros((len(r),len(r[0])))
    if kwargs[0] == 1 and kwargs[1] == 1:
        return r,g,b
    if kwargs[0] ==1 :
        kwargs[0] = 2
    if kwargs[1] ==1 :
        kwargs[1] = 2

    x = int(kwargs[0])//2
    y = int(kwargs[1])//2
    
    for i in range(y, len(r)-1-y):
        for j in range(x, len(r[i])-1-x):
            new_r[i][j] = np.median(r[i-y:i+y,j-x:j+x])
            new_g[i][j] = np.median(g[i-y:i+y,j-x:j+x])
            new_b[i][j] = np.median(b[i-y:i+y,j-x:j+x])
    return new_r, new_g, new_b

@njit(parallel=True, cache=True)
def jitmedianfilter(r,g,b, kwargs):
    new_r = np.zeros((len(r),len(r[0])))
    new_g = np.zeros((len(r),len(r[0])))
    new_b = np.zeros((len(r),len(r[0])))

    x = int(kwargs[0])//2
    y = int(kwargs[1])//2
    for i in prange(y, len(r)-1-y):
        # parkr= []
        # parkg= []
        # parkb= []
        for j in range(x, len(r[i])-1-x):
            new_r[i][j] = np.median(r[i-y:i+y,j-x:j+x])
            new_g[i][j] = np.median(g[i-y:i+y,j-x:j+x])
            new_b[i][j] = np.median(b[i-y:i+y,j-x:j+x])

        

    return new_r, new_g, new_b



img = np.random.rand(1000,1000,3)

r = img[:,:,0]
g = img[:,:,1]
b = img[:,:,2]

# print("Median filter: ", timeit.timeit(lambda: medianfilter(r,g,b, [3,3]), number=1))
times = []
counter = 2
for i in range(2, 50):
    t1 = time.time()
    jitmedianfilter(r,g,b, [counter+i, counter+i])
    
    t2 = time.time()
    times.append(t2-t1)
    print("Median filter: ", t2-t1)
import matplotlib.pyplot as plt
plt.plot(times)
plt.show()
# t1 = time.time()
# r,g,b = jitmedianfilter(r,g,b, [15, 15])
# t2 = time.time()
# create a image from rgb and show it 
import PIL
from PIL import Image
img = Image.fromarray(np.uint8(np.dstack((r,g,b))*255))
# increase the saturation 300%
img = img.convert("HSV")
h,s,v = img.split()
s = s.point(lambda i: i*3)
img = Image.merge("HSV", (h,s,v))
img = img.convert("RGB")
img.show()


print("JIT Median filter: ", t2-t1)
