import numpy as np
import matplotlib.pyplot as plt
from lif_model import lif
from utils import make_connectivity_matrix, connect_neurons

time = 1000
n = 4

neurons = [lif(ID) for ID in range(n)]
weights = np.linspace(1, -1.2, n)
cv = make_connectivity_matrix(weights, n)
connect_neurons(cv, neurons, n)


poissonInput = np.random.poisson(lam=1.0, size=time)
poissonWeight = 1.0
poissonConnections = [1, 2]

potentials = [[] for _ in range(n)]
for t in range(time):
    for neuron in neurons:

        if neuron.id in poissonConnections:
            neuron.Ip = poissonInput[t] * poissonWeight

        neuron.step()

        potentials[neuron.id].append(neuron.potential)


fig, axes = plt.subplots(n + 1, 1, figsize=(10, 10))

for i, ax in enumerate(axes[:-1]):
    ax.plot(potentials[i])
    ax.set_title(f"Voltage of neuron {i}")


for i in range(n):
    axes[-1].plot(potentials[i])
    axes[-1].set_title("Voltage of all neurons")

plt.show()