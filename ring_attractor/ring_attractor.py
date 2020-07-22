import numpy as np
import matplotlib.pyplot as plt
from lif_model import lif
from utils import make_connectivity_matrix, connect_neurons

time = 1000
n = 35

neurons = [lif(ID) for ID in range(n)]
weights = np.linspace(1, -1.2, n)
cv = make_connectivity_matrix(weights, n)
connect_neurons(cv, neurons, n)


poissonInput = np.random.poisson(lam=1.0, size=time)
poissonWeight = 1.0
poissonConnections = [4,5,6,7,8]

potentials = [[] for _ in range(n)]
for t in range(time):
    for neuron in neurons:

        if t < 200:
            if neuron.id in poissonConnections:
                neuron.Ip = poissonInput[t] * poissonWeight
        else:
            if neuron.id in poissonConnections:
                neuron.Ip = 0
            

        neuron.step()

        potentials[neuron.id].append(neuron.V)


fig, axes = plt.subplots(n, 1, figsize=(10, 10))

for i, ax in enumerate(axes):
    ax.plot(potentials[i])
    ax.set_ylabel(i)
    ax.set_yticklabels([])
    ax.set_yticks([])

plt.show()
