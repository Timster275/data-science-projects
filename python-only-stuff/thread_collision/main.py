import matplotlib.pyplot as plt
import numpy as np
from database import Database
from thread import Worker
from threading import Lock, Thread

import random
n = 2
n_max = 800
hits_for_n_runs = []
for j in range(0,n_max): 
    db = Database()
    l = Lock()
    workers = [Worker(i, db, l) for i in range(0,n)]
    threads = [Thread(target = workers[i].run) for i in range(0,n)]

    for t in threads:
        t.start()
    hits_for_n_runs.append(db.hits)
    # print(f"Finished run {j} with {db.hits} hits")
    n+=1


tdata = hits_for_n_runs
from sklearn.linear_model import LinearRegression
from scipy.signal import savgol_filter
sgdata = savgol_filter(tdata, 51, 3)
plt.plot(sgdata, label="Smoothed Data")
X = np.array([i for i in range(len(tdata))]).reshape(-1,1)
Y = np.array(tdata)
model = LinearRegression()
model.fit(X, Y)
X_future = np.array([i for i in range(len(tdata)+n_max+1000)]).reshape(-1,1)
Y_future = model.predict(X_future)

plt.plot(Y_future, label='Trend')
# plt.plot(tdata, label='Data')
plt.xlabel('Threads')
plt.ylabel('Collisions')
plt.legend()
plt.show()
