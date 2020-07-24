import numpy as np
from scipy import signal
import matplotlib.pyplot as plt



def check_connectivity(neurons):
    # TODO
    return


if __name__ == "__main__":
    # This is just to show the connectivity matrix
    n = 20
    # weights = signal.ricker(n, 4.0)
    weights = [0, 1, -1, -1, *[0 for _ in range(n-4)]]

    harvest = make_connectivity_matrix(weights, n)
    fig, ax = plt.subplots(figsize=(10, 10))
    im = ax.imshow(harvest)

    for i in range(n):
        for j in range(n):
            text = ax.text(j, i, round(harvest[i, j], 2),
                           ha="center", va="center", color="w")

    fig.tight_layout()
    plt.show()
