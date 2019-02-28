import numpy as np
import pandas as pd
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
from matplotlib import colors as mcolors

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

data = pd.read_csv("output_point.csv", names=['x','y','z','R','G','B'])
c = [mcolors.to_hex([r/255,g/255,b/255]) for r,g,b in zip(data.R, data.G, data.B)]
# ax.scatter(data.x, data.y, data.z, 'o', c=c)

data = np.random.random((500,6))
c = [mcolors.to_hex([r,g,b]) for r,g,b in data[:,3:]]
ax.scatter(data[:,0], data[:,1], data[:,2], 'o', c=c, s=25)


plt.show()

