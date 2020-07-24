import numpy as np
import matplotlib.pyplot as plt
from lif_drosophila import lif
from units import *

dt = 0.1 * ms
time = np.arange(0, 1, dt)
n = 2

neurons = [lif(ID) for ID in range(n)]

neurons[0].synapses[neurons[1]] = 1.0
neurons[1].synapses[neurons[0]] = 1.0


potentials = [[] for _ in range(n)]
for t in time:
    for neuron in neurons:

        neuron.Iex = 2.1 * nA

        neuron.step()

        potentials[neuron.id].append(neuron.V)


fig, axes = plt.subplots(n, 1, figsize=(10, 10))

for i, ax in enumerate(axes):
    ax.plot(potentials[i])

plt.show()

