import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from lif_model import LIF

n = 100
w = 0.08
dt = 1

neurons = [LIF(ID, dt=dt) for ID in range(n)]


for neur in neurons:
    for i in range(3, n/2):
        neur.synapses["inh"][neurons[(neur.id + i) % n]] = -w
        neur.synapses["inh"][neurons[neur.id - i]] = -w
    for i in range(1, 3):
        neur.synapses["exc"][neurons[(neur.id + i) % n]] = w
        neur.synapses["exc"][neurons[neur.id - i]] = w



conn = np.zeros([n,n])

for neur in neurons:
    for n, w in neur.synapses["inh"].items():
        assert conn[neur.id, n.id] == 0
        conn[neur.id, n.id] = w

    for n, w in neur.synapses["exc"].items():
        conn[neur.id, n.id] = w

fig = plt.figure(figsize=(10,10))
sns.heatmap(conn)
plt.show()
