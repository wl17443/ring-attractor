from LeakyIntegrateAndFireNeuron import *
import multiprocessing as mp
from ScalingTools import *
import numpy as np 
import matplotlib.pyplot as plt
manager = mp.Manager()

# Simulation times 
SIMULATION_TIME = 1
TIME_STEP = 0.25*ms
TOTAL_TIME_STEPS = np.linspace(0,SIMULATION_TIME,int(SIMULATION_TIME/TIME_STEP)+1)

NR_OF_LIAF_NEURONS = 2
LIAF_NEURONS = []
NEURON_SPIKE_TRAINS = []
PROCESSES = []


if __name__ == '__main__':
    # Initialising neurons 
    # TODO find a better way of defining siblings than this bs 
    for i in range(NR_OF_LIAF_NEURONS):
        LIAF_NEURONS.append(LeakyIntegrateAndFireNeuron(Id=i, siblings=[np.abs(i-1)], conns=None, main_conn=None))
        # TODO Connect neurons together     
    
    # Manually adding conns for two neurons 
    end1, end2 = mp.Pipe()
    LIAF_NEURONS[0].conns = end1
    LIAF_NEURONS[1].conns = end2
        # for j in range(len(LIAF_NEURONS[i].siblings)):
        #     par_con, child_con = mp.Pipe()
        #     LIAF_NEURONS[i].to_ends.append(par_con)
        #     LIAF_NEURONS[j].from_ends.append(child_con)

    pa1,c1 = mp.Pipe()
    pa2,c2 = mp.Pipe()

    LIAF_NEURONS[0].main_conn=c1
    LIAF_NEURONS[1].main_conn=c2

    p1 = mp.Process(target=LIAF_NEURONS[0].simulate)
    p2 = mp.Process(target=LIAF_NEURONS[1].simulate)

    p1.start()
    p2.start()

    spikeTrain1 = pa1.recv()
    spikeTrain2 = pa2.recv()

    T = 1
    dt = 0.25*ms 
    t = np.linspace(0,T,int(T/dt)+1)

    plt.plot(t,spikeTrain1)
    plt.plot(t,spikeTrain2)
    plt.show()