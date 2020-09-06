from mpl_toolkits import mplot3d
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


df = pd.read_csv("means.csv", index_col=0)


y = np.linspace(3,0,30)
x = df.index

X, Y = np.meshgrid(x, y)
Z = np.reshape(df.values.flatten(), X.shape)


fig = plt.figure()
ax = plt.axes(projection="3d")
ax.plot_surface(X, Y, Z)
ax.set_xlabel('Fixed points')
ax.set_ylabel('Noise')
ax.set_zlabel('Error')
# ax.plot_wireframe(X, Y, Z)
plt.show()
