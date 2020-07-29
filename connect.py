import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from LIF_Model import LIF


def connect_with_fixed_points(neurons, n, weights, fp_n=32):
    fp_idx = []
    if fp_n != 0:
        for i in range(n):
            if i % (n / fp_n) == 0:
                fp_idx.append(i - 1)
                fp_idx.append(i)
                fp_idx.append(i + 1)

    fixed_neurons = []
    for neur in neurons:
        if neur.id in fp_idx:
            fixed_neurons.append(neur)

# TODO use a matrix to do this shit
    for neur in neurons:
        if neur not in fixed_neurons:
            for i in range(5, 12):
                neur.synapses["inh"][neurons[(neur.id + i) % n]] = weights[1]
                neur.synapses["inh"][neurons[neur.id - i]] = weights[1]
            for i in range(1, 5):
                neur.synapses["exc"][neurons[(neur.id + i) % n]] = weights[0]
                neur.synapses["exc"][neurons[neur.id - i]] = weights[0]

    for neur in fixed_neurons:
        for i in range(5, 12):
            neur.synapses["inh"][neurons[(neur.id + i) % n]] = weights[3]
            neur.synapses["inh"][neurons[neur.id - i]] = weights[3]
        for i in range(1, 5):
            neur.synapses["exc"][neurons[(neur.id + i) % n]] = weights[2]
            neur.synapses["exc"][neurons[neur.id - i]] = weights[2]

    return fp_idx


if __name__ == "__main__":
    _n = 128
    dt = 1
    _weights = [1, -1, 5, -5]
    conn = np.zeros([_n, _n])
    _neurons = [LIF(ID, dt=dt) for ID in range(_n)]
    connect_with_fixed_points(_neurons, _n, _weights, fp_n=32)

    for _neur in _neurons:
        for n, w in _neur.synapses["inh"].items():
            conn[_neur.id, n.id] = w

        for n, w in _neur.synapses["exc"].items():
            conn[_neur.id, n.id] = w

    fig, ax = plt.subplots(1, figsize=(10, 10))

    sns.heatmap(conn, cmap="viridis", ax=ax[0])
    plt.show()
