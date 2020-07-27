import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from lif_model import LIF



def connect_with_fixed_points(neurons, n, weights, fp_n = 20):
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
            neur.synapses["inh"][neurons[(neur.id + i) % n]] = weights[1]
            neur.synapses["inh"][neurons[neur.id - i]] = weights[1]
        for i in range(1, 3):
            neur.synapses["exc"][neurons[(neur.id + i) % n]] = weights[0]
            neur.synapses["exc"][neurons[neur.id - i]] = weights[0]


    for neur in fixed_neurons:
        for i in range(3, 7):
            neur.synapses["inh"][neurons[(neur.id + i) % n]] = weights[3]
            neur.synapses["inh"][neurons[neur.id - i]] = weights[3]
        for i in range(1, 3):
            neur.synapses["exc"][neurons[(neur.id + i) % n]] = weights[2]
            neur.synapses["exc"][neurons[neur.id - i]] = weights[2]



if __name__ == "__main__":
    n = 100
    dt = 1
    weights = [1, -1, 5, -5]
    conn = np.zeros([n,n])
    neurons = [LIF(ID, dt=dt) for ID in range(n)]
    connect_with_fixed_points(neurons, n, weights)

    for neur in neurons:
        for n, w in neur.synapses["inh"].items():
            conn[neur.id, n.id] = w

        for n, w in neur.synapses["exc"].items():
            conn[neur.id, n.id] = w





    fig = plt.figure(figsize=(10,10))
    sns.heatmap(conn)
    plt.show()
