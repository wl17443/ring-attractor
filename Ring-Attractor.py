# Playground py file for a ring attractor  
import numpy as np
import matplotlib.pyplot as plt 
from ScalingTools import *
import random as rnd 
from scipy.stats import norm, vonmises 
import seaborn as sns; sns.set()

# Constants of neuron network 
NR_OF_NEURONS = 100

# Defining the connectivity using a 2-4 topology 
connectivity = np.zeros((NR_OF_NEURONS,NR_OF_NEURONS))
EXC = 1
INH = 3

for i in range(NR_OF_NEURONS):
    for j in range(i-INH, i+INH+1):
        if i!=j:
            if j >= NR_OF_NEURONS:
                connectivity[i,j%NR_OF_NEURONS] = 5
            else:
                connectivity[i,j] = -5

    for j in range(i-EXC, i+EXC+1):
        if i!=j:
            if j >= NR_OF_NEURONS:
                connectivity[i,j%NR_OF_NEURONS] = 5
            else:
                connectivity[i,j] = 5

# plt.imshow(connectivity)
# plt.show()

# Simulation parameters 
T = 0.25
dt = 0.25*ms
t = np.linspace(0,T,int(T/dt)+1)

SPIKE_TRAINS = np.zeros((NR_OF_NEURONS,len(t)))
OUTPUT_CURRENTS = np.zeros(NR_OF_NEURONS)

C_m = 0.002*mu_F # Me,brane capacitance 
V_0 = -52*mV # Resting potential 
R_m = 10*bigMOhm # Membrane resistance 
V_thr = -45 *mV # Firing threshold 
V_max = 20*mV # Peak action potential 
V_min = -72*mV # Spike undershoot voltage 
t_AP = 2*ms # Length of an action potential 
I_PSC = 5*nA
t_PSC = 5*ms

def M_jI_j(i):
    return (connectivity[:,i]*OUTPUT_CURRENTS).sum()

def f(v_i, I_in, i):
    return ((V_0-v_i)/R_m+I_in+M_jI_j(i))/C_m

def v(t):
    if t > 0 and t < t_AP/2:
        # rdf = np.random.normal(-1+t/t_AP/2,1)
        rdf = norm.pdf(-1+t/t_AP/2, 0, 1)
        return V_thr+(V_max-V_min)*rdf
    elif t > t_AP/2 and t < t_AP:
        return V_min + (V_max-V_min)*(np.sin((t-t_AP/2)*(2*np.pi/t_AP)+np.pi/2)+1)/2

def I(t):
    if t > 0 and t < 2:
        return I_PSC*np.sin(t*np.pi/2-np.pi/2)
    elif t > 2 and t <= 2+7*t_PSC:
        return I_PSC*2**(-(t-2)/t_PSC)
    else: return 0 

LAST_SPIKE = np.zeros(NR_OF_NEURONS)
INPUT_CURRENT = np.zeros((NR_OF_NEURONS,len(t)))

# Initialise external input current 
kappa = 3.99
rs = vonmises.rvs(kappa, loc=0, scale=0.1, size=NR_OF_NEURONS)
for r in rs:
    INPUT_CURRENT[int(r*NR_OF_NEURONS),0:100] = 1*nA
# rs = vonmises.rvs(kappa, loc=0, scale=0.5, size=NR_OF_NEURONS)
# for r in rs:
#     INPUT_CURRENT[int(r*NR_OF_NEURONS),101:200] = 1*nA
 
def simulate():
    SPIKE_TRAINS[:,0] = V_0
    for time in range(1,len(t)):
        for neuron in range(NR_OF_NEURONS):
            if SPIKE_TRAINS[neuron,time-1] >= V_thr:
                SPIKE_TRAINS[neuron,time] = v(time*dt-LAST_SPIKE[neuron])
                OUTPUT_CURRENTS[neuron] = I(time*dt-LAST_SPIKE[neuron])
            else: 
                SPIKE_TRAINS[neuron,time] = SPIKE_TRAINS[neuron,time-1]+f(SPIKE_TRAINS[neuron,time-1],INPUT_CURRENT[neuron,time-1],neuron)*dt
                if SPIKE_TRAINS[neuron,time] >= V_thr:
                    LAST_SPIKE[neuron] = time*dt

if __name__ == "__main__":
    simulate()
    # fig, axs = plt.subplots(NR_OF_NEURONS)
    # for i in range(NR_OF_NEURONS):
    #     axs[i].plot(t,SPIKE_TRAINS[i]) 
    ax = sns.heatmap(SPIKE_TRAINS)
    plt.show()
    
