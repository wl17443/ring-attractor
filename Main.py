from LeakyIntegrateAndFireNeuron import *
import multiprocessing as mp
from ScalingTools import *
import numpy as np 
import matplotlib.pyplot as plt
import random as rnd 
from Dictionaries import *
# Simulation times 
SIMULATION_TIME = 1
dt = 0.25*ms 
t = np.linspace(0,SIMULATION_TIME,int(SIMULATION_TIME/dt)+1)
def SimulateLayeredNeuronNetwork():
    NETWORK_STRUCTURE = [2, 1]
    NR_OF_LIAF_NEURONS = np.sum(NETWORK_STRUCTURE)
    LIAF_NEURONS = []
    NEURON_SPIKE_TRAINS = []
    PROCESSES = []

    # Initialising neurons 
    MOTHER_PROCESS_CONN_ENDS = []

    for i in range(NR_OF_LIAF_NEURONS):
        # Create mother to children processes pipes 
        pa,c = mp.Pipe()
        MOTHER_PROCESS_CONN_ENDS.append(pa)
        # Randomly choose which neurons are excitatory/inhibitory according to a probability (?)
        LIAF_NEURONS.append(LeakyIntegrateAndFireNeuron(Id=i, neuron_params=neuronParams, simulation_time=SIMULATION_TIME, to_siblings_conns=[], from_siblings_conns=[], main_conn=c))
    
    # TODO connect to a random number of next layer neurons determined by user 
    # This ultimately defines how the neurons are connected to each other 
    if len(NETWORK_STRUCTURE) > 1:
        for layer_nr in range(len(NETWORK_STRUCTURE)-1):
            for neuron_nr in range(NETWORK_STRUCTURE[layer_nr]):
                end1, end2 = mp.Pipe()
                LIAF_NEURONS[neuron_nr].to_siblings_conns.append(end1)
                LIAF_NEURONS[(layer_nr+1)*NETWORK_STRUCTURE[layer_nr]].from_siblings_conns.append(end2)

    # Start parallelised neuron processes
    for neuron in LIAF_NEURONS:
        PROCESSES.append(mp.Process(target=neuron.simulate))
    for process in PROCESSES:
        process.start()

    for i in range(len(MOTHER_PROCESS_CONN_ENDS)):
        spikeTrain = MOTHER_PROCESS_CONN_ENDS[i].recv()
        NEURON_SPIKE_TRAINS.append(spikeTrain)
        plt.plot(t, spikeTrain, label="Neuron"+str(i))

    # TODO implement a live spike train presenter (?)
    plt.legend()
    plt.show()

def SimulateRingModel():
    NR_OF_NEURONS = 5
    MOTHER_PROCESS_CONN_ENDS = []
    LIAF_NEURONS = []
    for i in range(NR_OF_NEURONS):
        pa, c = mp.Pipe()
        MOTHER_PROCESS_CONN_ENDS.append(pa)
        LIAF_NEURONS.append(LeakyIntegrateAndFireNeuron(Id=i, neuron_params=neuronParams, simulation_time=SIMULATION_TIME, to_siblings_conns=[], from_siblings_conns=[], main_conn=c))

    # Define connections so they are in a ring - 1 layer for now 
    for i in range(NR_OF_NEURONS):
        for j in range(NR_OF_NEURONS):
            if i != j:
                end1, end2 = mp.Pipe()
                LIAF_NEURONS[i].to_siblings_conns.append(end1)
                LIAF_NEURONS[j].from_siblings_conns.append(end2)

    