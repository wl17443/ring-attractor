import numpy as np 

# Function to make connectivity matrix of a ring attractor
#   Where 0 means no connection, -1 means inhibitory synapse, and 1 means excitatory synapse
def make_connectivity_matrix(nr_of_neurons, nr_of_inhibitory, nr_of_excitatory):
    matrix = np.zeros((nr_of_neurons, nr_of_neurons))
    
    for i in range(nr_of_neurons):
        for j in range(i-nr_of_inhibitory, i+nr_of_inhibitory+1):
            if i!=j:
                if j >= nr_of_neurons:
                    matrix[i,j%nr_of_neurons] = -1
                else:
                    matrix[i,j] = -1
        for j in range(i-nr_of_excitatory, i+nr_of_excitatory+1):
            if i!=j:
                if j >= nr_of_neurons:
                    matrix[i,j%nr_of_neurons] = 1
                else:
                    matrix[i,j] = 1

    return matrix 
