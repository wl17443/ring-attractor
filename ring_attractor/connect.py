
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from lif_model import LIF

#   python C:\Users\Nikitas\Desktop\NEW\CODE\connect.py

import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from lif_model import LIF


def calculate_weights(weights, fp_n=16,total_neurons = 128):
    if fp_n>=1:
        print("it_works")
        new_weights = [0, 0, 0, 0]
        new_weights[0] = 0.9*weights[0]
        new_weights[1] = 0.9*weights[1]
        new_weights[2] = (0.1*total_neurons/fp_n + 1)*weights[0]
        new_weights[3] = (0.1*total_neurons/fp_n + 1)*weights[1]
    else:
        new_weights = weights
    return new_weights

def connect_with_fixed_points(neurons, n, weights, fp_n = 16):
    fp_idx = []
    if fp_n != 0:
        for i in range(n):
            if i % (n / fp_n) == 0:
                fp_idx.append(i)

    print(fp_idx)

    weights = calculate_weights(weights, fp_n, n)
    fixed_neurons = []
    for neur in neurons:
        if neur.id in fp_idx:
            fixed_neurons.append(neur)

    for neur in neurons:
        if neur not in fixed_neurons:
            for i in range(8, 12):
                neur.synapses["inh"][neurons[(neur.id + i) % n]] = weights[1]*np.exp(-0.5-(i-9)/4)*1.5
                neur.synapses["inh"][neurons[neur.id - i]] = weights[1]*np.exp(-0.5-(i-9)/4)*1.5
            for i in range(5, 8):
                neur.synapses["inh"][neurons[(neur.id + i) % n]] = weights[1]*np.log(2+(i-5)/3)*1.5
                neur.synapses["inh"][neurons[neur.id - i]] = weights[1]*np.log(2+(i-5)/3)*1.5
            for i in range(1, 5):
                neur.synapses["exc"][neurons[(neur.id + i) % n]] = weights[0]*np.log(2-(i)/5)*1.5
                neur.synapses["exc"][neurons[neur.id - i]] = weights[0]*np.log(2-(i)/5)*1.5


    for neur in fixed_neurons:
        for i in range(8, 12):
                neur.synapses["inh"][neurons[(neur.id + i) % n]] = weights[3]*np.exp(-0.5-(i-9)/4)*1.5
                neur.synapses["inh"][neurons[neur.id - i]] = weights[3]*np.exp(-0.5-(i-9)/4)*1.5
        for i in range(5, 8):
            neur.synapses["inh"][neurons[(neur.id + i) % n]] = weights[3]*np.log(2+(i-5)/3)*1.5
            neur.synapses["inh"][neurons[neur.id - i]] = weights[3]*np.log(2+(i-5)/3)*1.5
        for i in range(1, 5):
            neur.synapses["exc"][neurons[(neur.id + i) % n]] = weights[2]*np.log(2-(i)/5)*1.5
            neur.synapses["exc"][neurons[neur.id - i]] = weights[2]*np.log(2-(i)/5)*1.5

    return fp_idx



if __name__ == "__main__":
    n = 128
    dt = 1
    weights = [1, -1, 5, -5]
    conn = np.zeros([n,n])
    neurons = [LIF(ID, dt=dt) for ID in range(n)]
    connect_with_fixed_points(neurons, n, weights, fp_n=8)

    for neur in neurons:
        for n, w in neur.synapses["inh"].items():
            conn[neur.id, n.id] = w

        for n, w in neur.synapses["exc"].items():
            conn[neur.id, n.id] = w





    fig = plt.figure(figsize=(10,10))
    sns.heatmap(conn, cmap="viridis") 
    plt.show()