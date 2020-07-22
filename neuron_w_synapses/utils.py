import numpy as np
import matplotlib.pyplot as plt

def kth_diag_indices(a, k):
    rows, cols = np.diag_indices_from(a)
    if k < 0:
        return rows[-k:], cols[:k]
    elif k > 0:
        return rows[:-k], cols[k:]
    else:
        return rows, cols

def make_connectivity_matrix(weights, n):
    connectivity_matrix = np.zeros([n,n])

    for i, w in enumerate(weights):
        connectivity_matrix[kth_diag_indices(connectivity_matrix, i)] = w
        connectivity_matrix[kth_diag_indices(connectivity_matrix, -i)] = w

    connectivity_matrix[connectivity_matrix < -1.01] = 0.0
    return connectivity_matrix


def connect_neurons(cv, neurons, n):
    for row in range(n):
        for col in range(n):

            # We don't want neurons connected to themselves
            if row == col:
                continue
            neurons[row].synapses[neurons[col]] = cv[row, col]
            neurons[col].synapses[neurons[row]] = cv[col, row]
    


def check_connectivity(neurons):
    #TODO
    return

if __name__ == "__main__":
    n = 12
    harvest = make_connectivity_matrix(np.linspace(1,-1.6,n), n)
    fig, ax = plt.subplots(figsize=(10,10))
    im = ax.imshow(harvest)



# Loop over data dimensions and create text annotations.
    for i in range(n):
        for j in range(n):
            text = ax.text(j, i, round(harvest[i, j], 2),
                           ha="center", va="center", color="w")

    fig.tight_layout()
    plt.show()
