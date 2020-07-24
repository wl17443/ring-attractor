import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from lif_model import LIF

time = 300
n = 100
w = 0.08
spike_source = [c for c in range(30,41)]

neurons = [LIF(ID, dt=0.25) for ID in range(n)]


for neur in neurons:
    for i in range(1, 3):
        neur.synapses[neurons[(neur.id + i) % n]] = w
        neur.synapses[neurons[neur.id - i]] = w

    for i in range(3, 7):
        neur.synapses[neurons[(neur.id + i) % n]] = -w
        neur.synapses[neurons[neur.id - i]] = -w


potentials = [[] for _ in range(n)]
for t in range(time):
    for neuron in neurons:

        if neuron.id in spike_source:
            neuron.exc_ps_td.append((t * 1e-3, w))

        
        neuron.step()

        potentials[neuron.id].append(neuron.V)


# Plots
fig, ax = plt.subplots(figsize=(10, 10))
df = pd.DataFrame(potentials)
sns.heatmap(df, vmin=-0.08, vmax=0.0, cmap="viridis")
plt.show()

