from numba import njit
import numpy as np
import timeit
@njit
def numba_sum(a):
    s = 0
    for i in range(a.shape[0]):
        s += a[i]
    return s

from numba import jit
@jit
def jit_sum(a):
    s = 0
    for i in range(a.shape[0]):
        s += a[i]
    return s


def python_sum(a):
    s = 0
    for i in range(a.shape[0]):
        s += a[i]
    return s

a = np.random.rand(1000000)

print("Numba sum: ", timeit.timeit(lambda: numba_sum(a), number=100))
print("JIT sum: ", timeit.timeit(lambda: jit_sum(a), number=100))
print("Python sum: ", timeit.timeit(lambda: python_sum(a), number=100))


