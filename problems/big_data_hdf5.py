import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import pandas as pd
import time

t0 = time.time()
fig = plt.figure()
ax = fig.add_subplot(111)

data = pd.read_hdf("test.hdf5", "table/t1")
print(data.shape)
print(time.time() - t0)
rows, cols = data.shape
period = 7200
i0 = 0
theta = data.Theta[:period]
for i in range(rows//period):
    ax.plot(theta, data.p_Cyl1[i*period:(i+1)*period], lw=1, c='gray')
plt.show()