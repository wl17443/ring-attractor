import numpy as np
import matplotlib.pyplot as plt

def get_indeces_of_kth_diagonal(a, k):
    # Copypasted from stack overflow :)
    rows, cols = np.diag_indices_from(a)
    if k < 0:
        return rows[-k:], cols[:k]
    elif k > 0:
        return rows[:-k], cols[k:]
    else:
        return rows, cols

def make_connectivity_matrix(weights, n):
    # Probably won't be used later, automatically set up a connectivity matrix 
    connectivity_matrix = np.zeros([n,n])

    for i, w in enumerate(weights):
        connectivity_matrix[get_indeces_of_kth_diagonal(connectivity_matrix, i)] = w
        connectivity_matrix[get_indeces_of_kth_diagonal(connectivity_matrix, -i)] = w

    # connectivity_matrix[connectivity_matrix < -1.01] = 0.0
    return connectivity_matrix


def connect_neurons(connectivity_matrix, neurons, n):

    for row in range(n):
        for col in range(n):

            # We don't want neurons connected to themselves
            if row == col:
                continue
            neurons[row].synapses[neurons[col]] = connectivity_matrix[row, col]
            neurons[col].synapses[neurons[row]] = connectivity_matrix[col, row]
    


def check_connectivity(neurons):
    #TODO
    return

if __name__ == "__main__":
    # This is just to show the connectivity matrix
    n = 12
    harvest = make_connectivity_matrix(np.linspace(1,-1.6,n), n)
    fig, ax = plt.subplots(figsize=(10,10))
    im = ax.imshow(harvest)

    for i in range(n):
        for j in range(n):
            text = ax.text(j, i, round(harvest[i, j], 2),
                           ha="center", va="center", color="w")

    fig.tight_layout()
    plt.show()
