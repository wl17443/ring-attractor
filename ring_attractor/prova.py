import numpy as np
import matplotlib.pyplot as plt
from lif_model import lif
import pandas as pd

time = 500
n = 2

neurons = [lif(ID) for ID in range(n)]

neurons[0].synapses[neurons[1]] = 1 
neurons[1].synapses[neurons[0]] = 1 


potentials = [[] for _ in range(n)]
synpot = [[] for _ in range(n)]
for t in range(time):
    for neuron in neurons:
        neuron.Iext = 1.9 * 1e-9

        neuron.step()

        potentials[neuron.id].append(neuron.V)
        synpot[neuron.id].append(neuron.Is_exc)


fig, axes = plt.subplots(n, 1, figsize=(10, 10))

for i, ax in enumerate(axes):
    ax.plot(potentials[i])
plt.show()

fig, axes = plt.subplots(n, 1, figsize=(10, 10))

for i, ax in enumerate(axes):
    ax.plot(synpot[i])
plt.show()


