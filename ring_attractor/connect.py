
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


def see_neurons(A, ax, ratio_observed=1, arrows=True):
    """
    Visualizes the connectivity matrix.

    Args:
        A (np.ndarray): the connectivity matrix of shape (n_neurons, n_neurons)
        ax (plt.axis): the matplotlib axis to display on

    Returns:
        Nothing, but visualizes A.
    """
    n = len(A)

    ax.set_aspect('equal')
    thetas = np.linspace(0, np.pi * 2, n, endpoint=False)
    x, y = np.cos(thetas), np.sin(thetas),
    if arrows:
      for i in range(n):
          for j in range(n):
              if A[i, j] > 0:
                  ax.arrow(x[i], y[i], x[j] - x[i], y[j] - y[i], color='k', head_width=.05,
                          width = A[i, j] / 25,shape='right', length_includes_head=True,
                          alpha = .2)
    if ratio_observed < 1:
      nn = int(n * ratio_observed)
      ax.scatter(x[:nn], y[:nn], c='r', s=150, label='Observed')
      ax.scatter(x[nn:], y[nn:], c='b', s=150, label='Unobserved')
      ax.legend(fontsize=15)
    else:
      ax.scatter(x, y, c='k', s=150)
    ax.axis('off')


def connect_with_fixed_points(neurons, n, weights, fp_n = 32):
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
    n = 128
    dt = 1
    weights = [1, -1, 5, -5]
    conn = np.zeros([n,n])
    neurons = [LIF(ID, dt=dt) for ID in range(n)]
    connect_with_fixed_points(neurons, n, weights, fp_n=32)

    for neur in neurons:
        for n, w in neur.synapses["inh"].items():
            conn[neur.id, n.id] = w

        for n, w in neur.synapses["exc"].items():
            conn[neur.id, n.id] = w




    fig, ax = plt.subplots(2, figsize=(10,10))

    see_neurons(conn, ax[1])

    sns.heatmap(conn, cmap="viridis", ax = ax[0]) 
    plt.show()
