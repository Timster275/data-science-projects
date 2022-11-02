def times_cy(r,g,b, times):
    tr = []
    tg = []
    tb = []
    for i in range(0, len(r)-1):
        temp_r = []
        temp_g = []
        temp_b = []
        for j in range(0, len(r[i])-1):
            temp_r.append(r[i][j] * times)
            temp_g.append(g[i][j] * times)
            temp_b.append(b[i][j] * times)
        tr.append(temp_r)
        tg.append(temp_g)
        tb.append(temp_b)

    return tr, tg, tb
