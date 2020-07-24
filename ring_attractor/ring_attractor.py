import numpy as np
import matplotlib.pyplot as plt
from lif_model import lif
from utils import make_connectivity_matrix, connect_neurons
import pandas as pd
from scipy import signal

time = 1000
n = 20

neurons = [lif(ID) for ID in range(n)]
# weights = signal.ricker(n, 4.0)
weights = [0, 1, 1, -1, -1, -1, -1, *[0 for _ in range(n-7)]]

# cv = make_connectivity_matrix(weights, n)
# connect_neurons(cv, neurons, n)

for neur in neurons:
    for i in range(1, 3):
        neur.synapses[neurons[(neur.id + i) % n]] = 1
        neur.synapses[neurons[neur.id - i]] = 1

    for i in range(3, 7):
        neur.synapses[neurons[(neur.id + i) % n]] = -1
        neur.synapses[neurons[neur.id - i]] = -1


potentials = [[] for _ in range(n)]
for t in range(time):
    for neuron in neurons:
        if neuron.id == 0:
            if t < 200:
                neuron.Iext = 1.9 * 1e-9
            if t > 200:
                neuron.Iext = 0

        neuron.step()

        potentials[neuron.id].append(neuron.V)


fig, axes = plt.subplots(n, 1, figsize=(10, 10))

for i, ax in enumerate(axes):
    ax.plot(potentials[i])
    ax.set_ylabel(i)
    ax.set_yticklabels([])
    ax.set_yticks([])

plt.show()

df = pd.DataFrame(potentials)
spikes = (df == 0.0).astype(int) * np.arange(time)
plt.eventplot(np.array(spikes))
plt.show()
