import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import pandas as pd
import time

t0 = time.time()
fig = plt.figure()
ax = fig.add_subplot(111)

period = 7200
i0 = 0
table = "table/t1"
data = pd.read_hdf("test.hdf5", table, start=0, stop=period)
print(data.shape)
theta = data.Theta
average, N = 0, 100
for i in range(N):
    data = pd.read_hdf("test.hdf5", table, start=i*period, stop=(i+1)*period)
    data = data.p_Cyl1
    average += data.values
    ax.plot(theta, data, lw=1, c='gray')
ax.plot(theta, average/N, lw=1, c='r')
print(time.time() - t0)
plt.show()