import numpy as np
def timeso5(r,g,b, times):
    times = times['times']
    new_r = np.zeros((len(r),len(r[0])))
    new_g = np.zeros((len(r),len(r[0])))
    new_b = np.zeros((len(r),len(r[0])))
    for i in range(0, len(r)-1):
        for j in range(0, len(r[i])-1):
            new_r[i][j] = r[i][j] * times
            new_g[i][j] = g[i][j] * times
            new_b[i][j] = b[i][j] * times
    return np.asarray(new_r), np.asarray(new_g), np.asarray(new_b)

def savgolfilter(r,g,b, kwargs):
    from scipy.signal import savgol_filter
    new_r = savgol_filter(r, int(kwargs['window_length']), kwargs['polyorder'])
    new_g = savgol_filter(g, int(kwargs['window_length']), kwargs['polyorder'])
    new_b = savgol_filter(b, int(kwargs['window_length']), kwargs['polyorder'])
    return new_r, new_g, new_b

## RGB CHANNEL MIXER 