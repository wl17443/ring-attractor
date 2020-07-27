import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from lif_model import LIF

n = 100
dt = 1

ew = 1
iw = -1
fp_ew = 5
fp_iw = -5


def connect_with_fixed_points(neurons, n, fp_n = 20):
    fp_idx = []
    for i in range(n):
        if i % fp_n == 0:
            fp_idx.append(i)


    fixed_neurons = []
    for neur in neurons:
        if neur.id in fp_idx:
            fixed_neurons.append(neur)

    for neur in neurons:
        for i in range(3, 7):
            neur.synapses["inh"][neurons[(neur.id + i) % n]] = iw
            neur.synapses["inh"][neurons[neur.id - i]] = iw
        for i in range(1, 3):
            neur.synapses["exc"][neurons[(neur.id + i) % n]] = ew
            neur.synapses["exc"][neurons[neur.id - i]] = ew


    for neur in fixed_neurons:
        for i in range(3, 7):
            neur.synapses["inh"][neurons[(neur.id + i) % n]] = fp_iw
            neur.synapses["inh"][neurons[neur.id - i]] = fp_iw
        for i in range(1, 3):
            neur.synapses["exc"][neurons[(neur.id + i) % n]] = fp_ew
            neur.synapses["exc"][neurons[neur.id - i]] = fp_ew



if __name__ == "__main__":
    n = 100
    conn = np.zeros([n,n])
    neurons = [LIF(ID, dt=dt) for ID in range(n)]
    connect_with_fixed_points(neurons, n)

    for neur in neurons:
        for n, w in neur.synapses["inh"].items():
            conn[neur.id, n.id] = w

        for n, w in neur.synapses["exc"].items():
            conn[neur.id, n.id] = w





    fig = plt.figure(figsize=(10,10))
    sns.heatmap(conn)
    plt.show()
