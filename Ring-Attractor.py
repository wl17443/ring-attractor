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
EXC = 10
INH = 20

for i in range(NR_OF_NEURONS):
    # for j in range(NR_OF_NEURONS):
    #     connectivity[i,j] = -15 

    for j in range(i-INH, i+INH+1):
        if i!=j:
            if j >= NR_OF_NEURONS:
                connectivity[i,j%NR_OF_NEURONS] = -15
            else:
                connectivity[i,j] = -15
        else:
            connectivity[i,j] = 0 

    for j in range(i-EXC, i+EXC+1):
        if i!=j:
            if j >= NR_OF_NEURONS:
                connectivity[i,j%NR_OF_NEURONS] = 20
            else:
                connectivity[i,j] = 20
        elif i==j:
            connectivity[i,j] = 0 

# ax = sns.heatmap(connectivity)
# plt.show()

# Simulation parameters 
T = 1
dt = 0.1*ms
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

# def normpdf(mu, sigma, x):
#     return (np.exp(-(x-mu)**2)/(2*sigma**2))/(sigma*np.sqrt(2*np.pi))

def M_jI_j(i):
    return (np.multiply(connectivity[:,i],OUTPUT_CURRENTS)).sum()

def f(v_i, I_in, i):
    return ((V_0-v_i)/R_m+I_in+M_jI_j(i))/C_m

def v(t):
    if t > 0 and t <= t_AP/2:
        return V_thr+(V_max-V_min)*norm.pdf(-1+t/t_AP/2,0,1)
    elif t > t_AP/2 and t < t_AP:
        return V_min + (V_max-V_min)*(np.sin((t-t_AP/2)*(2*np.pi/t_AP)+np.pi/2)+1)/2
    else: return V_min 

def I(t):
    if t > 0 and t < 2:
        return I_PSC*(np.sin(t*np.pi/2-np.pi/2)+1)/2
    elif t > 2 and t <= 2+7*t_PSC:
        return I_PSC*(2**(-(t-2)/t_PSC))
    else: return 0 

LAST_SPIKE = np.zeros(NR_OF_NEURONS)
INPUT_CURRENT = np.zeros((NR_OF_NEURONS,len(t)))
SPIKED = [False] * NR_OF_NEURONS 

pdf = range(30,40)
for r in pdf:
    INPUT_CURRENT[r,0] = 5*nA

def simulate():
    SPIKE_TRAINS[:,0] = V_0
    for time in range(1,len(t)):
        for neuron in range(NR_OF_NEURONS):
            if SPIKE_TRAINS[neuron,time-1] >= V_thr:
                if not SPIKED[neuron]:
                    SPIKED[neuron] = True 
                    LAST_SPIKE[neuron] = (time-1)*dt
                SPIKE_TRAINS[neuron,time] = v(time*dt-LAST_SPIKE[neuron])
                OUTPUT_CURRENTS[neuron] += I(time*dt-LAST_SPIKE[neuron])
            else: 
                SPIKED[neuron] = False 
                OUTPUT_CURRENTS[neuron] += I(time*dt-LAST_SPIKE[neuron])
                SPIKE_TRAINS[neuron,time] = SPIKE_TRAINS[neuron,time-1]+f(v_i=SPIKE_TRAINS[neuron,time-1],I_in=SPIKE_TRAINS[neuron,time-1], i=neuron)*dt


if __name__ == "__main__":
    simulate()
    # fig, axs = plt.subplots(NR_OF_NEURONS)
    # for i in range(NR_OF_NEURONS):
    #     axs[i].plot(t,SPIKE_TRAINS[i]) 
    ax = sns.heatmap(SPIKE_TRAINS)
    plt.show()
