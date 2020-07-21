from LeakyIntegrateAndFireNeuron import *
import multiprocessing as mp
from ScalingTools import *
import numpy as np 
import matplotlib.pyplot as plt
manager = mp.Manager()

# Simulation times 
SIMULATION_TIME = 1
TIME_STEP = 0.25*ms
TOTAL_TIME_STEPS = np.linspace(0, SIMULATION_TIME, int(SIMULATION_TIME/TIME_STEP)+1)

NR_OF_LIAF_NEURONS = 2
LIAF_NEURONS = []
NEURON_SPIKE_TRAINS = []
PROCESSES = []
LAYERS = 2 

T = 1
dt = 0.25*ms 
t = np.linspace(0,T,int(T/dt)+1)


if __name__ == '__main__':
    # Initialising neurons 
    # TODO find a better way of defining siblings than this bs 
    MOTHER_PROCESS_CONN_ENDS = []

    for i in range(NR_OF_LIAF_NEURONS):
        # Create mother to children processes pipes 
        pa,c = mp.Pipe()
        MOTHER_PROCESS_CONN_ENDS.append(pa)
        LIAF_NEURONS.append(LeakyIntegrateAndFireNeuron(Id=i, siblings=[np.abs(i-1)], sibling_conns=None, main_conn=c))
    
    # TODO automatically connect neurons together and to the main process 
    # TODO connect to a random number of next layer neurons 
    # TODO randomly choose which neurons are excitatory/inhibitory 
    # Manually adding conns for two neurons 
    end1, end2 = mp.Pipe()
    LIAF_NEURONS[0].sibling_conns = end1
    LIAF_NEURONS[1].sibling_conns = end2
        # for j in range(len(LIAF_NEURONS[i].siblings)):
        #     par_con, child_con = mp.Pipe()
        #     LIAF_NEURONS[i].to_ends.append(par_con)
        #     LIAF_NEURONS[j].from_ends.append(child_con)

    # TODO Create a layer of neurons to a single neuron 

    # Start parallelised neuron processes
    p1 = mp.Process(target=LIAF_NEURONS[0].simulate)
    p2 = mp.Process(target=LIAF_NEURONS[1].simulate)

    p1.start()
    p2.start()

    for pa in MOTHER_PROCESS_CONN_ENDS:
        spikeTrain = pa.recv()
        NEURON_SPIKE_TRAINS.append(spikeTrain)
        plt.plot(t, spikeTrain)

    # TODO implement a live spike train presenter (?)
    plt.show()