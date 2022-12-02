import numpy as np
def timeso5(r,g,b, times):
    times = times['times']
    new_r = np.zeros((len(r),len(r[0])))
    new_g = np.zeros((len(r),len(r[0])))
    new_b = np.zeros((len(r),len(r[0])))
    print(r[0][0:10])
    for i in range(0, len(r)-1):
        for j in range(0, len(r[i])-1):
            new_r[i][j] = r[i][j] * times
            new_g[i][j] = g[i][j] * times
            new_b[i][j] = b[i][j] * times
    print(new_r[0][0:10])
    return np.asarray(new_r), np.asarray(new_g), np.asarray(new_b)

def savgolfilter(r,g,b, kwargs):
    from scipy.signal import savgol_filter
    new_r = []
    new_g = []
    new_b = []
    for i in range(0, len(r)-1):
        new_r.append(savgol_filter(r[i], int(kwargs['window_length']), kwargs['polyorder']))
        new_g.append(savgol_filter(g[i], int(kwargs['window_length']), kwargs['polyorder']))
        new_b.append(savgol_filter(b[i], int(kwargs['window_length']), kwargs['polyorder']))
    return np.asarray(new_r), np.asarray(new_g), np.asarray(new_b)

def medianfilter(r,g,b, kwargs):
    r = np.asarray(r)
    g = np.asarray(g)
    b = np.asarray(b)
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
    
    print(r[0][0:10])
    for i in range(y, len(r)-1-y):
        for j in range(x, len(r[i])-1-x):
            new_r[i][j] = np.median(r[i-y:i+y,j-x:j+x])
            new_g[i][j] = np.median(g[i-y:i+y,j-x:j+x])
            new_b[i][j] = np.median(b[i-y:i+y,j-x:j+x])
    return new_r, new_g, new_b

## RGB CHANNEL MIXER 