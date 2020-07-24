# Playground py file for a ring network 
import numpy as np
import matplotlib.pyplot as plt 
from ScalingTools import *
import random as rnd 

# Constants of neuron network 
NR_OF_NEURONS = 20
EXC = 2
INH = 6
# Defining the connectivity using a 2-4 topology 
connectivity = np.zeros((NR_OF_NEURONS,NR_OF_NEURONS))
for i in range(NR_OF_NEURONS):
    for j in range(i-INH, i+INH+1):
        if i!=j:
            if j >= NR_OF_NEURONS:
                connectivity[i,j%NR_OF_NEURONS] = -1
            else:
                connectivity[i,j] = -1 

    for j in range(i-EXC, i+EXC+1):
        if i!=j:
            if j >= NR_OF_NEURONS:
                connectivity[i,j%NR_OF_NEURONS] = 1
            else:
                connectivity[i,j] = 1 

# plt.matshow(connectivity)
# plt.show()

T = 0.5
dt = 0.25*ms
t = np.linspace(0,T,int(T/dt)+1)

SPIKE_TRAINS = np.zeros((NR_OF_NEURONS, len(t)))
LAST_SPIKE = np.zeros(NR_OF_NEURONS)
LAST_SPIKE[:] = -100 

# Neuron parameters 
v_thresh = -48*mV
T_refract = 2*ms 
C_m = 1*nF
V_reset = -70*mV
V_rest = -65*mV
E_rev_ex = 0*mV
E_rev_in = -70*mV
T_syn_ex = T_syn_in = 5*ms
T_m = 20*ms
# This needs changing to a learning rule 
k_ex = 1/(T_syn_ex*np.exp(-1))
k_in = 1/(T_syn_in*np.exp(-1))

def I_syn_ex(V_m, neuron, t):
    return G_ex(neuron, t)*(V_m-E_rev_ex)

def I_syn_in(V_m, neuron, t):
    return G_in(neuron, t)*(V_m-E_rev_in)

def I_leak(V_m):
    return (C_m*(V_m-V_rest))/T_m

def G_ex(neuron, t):
    return k_ex*t*dt*np.exp(-t*dt/T_syn_ex)

def G_in(neuron, t):
    return k_in*t*dt*np.exp(-t*dt/T_syn_in)

def f(I_leak, I_syn, I_ext):
    return (-I_leak-I_syn+I_ext)/C_m

def I_syn(neuron, V_m, t):
    sum = 0 
    for connected in range(len(connectivity[neuron])):
        if connectivity[neuron, connected] == 1:
            sum += I_syn_ex(V_m, connected, t)
        elif connectivity[neuron, connected] == -1:
            sum += I_syn_in(V_m, connected, t)
    return sum 

def r(neuron):
    if neuron%5==0:
        return 1*nA
    else:
        return 0 

def simulate():
    SPIKE_TRAINS[:,0] = V_rest
    REFRACTORY_TIMES = np.zeros(NR_OF_NEURONS)

    for time in range(1, len(t)):
        for neuron in range(NR_OF_NEURONS):
            if REFRACTORY_TIMES[neuron] > 0:
                REFRACTORY_TIMES[neuron] -= dt
                SPIKE_TRAINS[neuron,time] = SPIKE_TRAINS[neuron,time-1]+f(I_leak(SPIKE_TRAINS[neuron,time-1]),0,0)*dt
            if SPIKE_TRAINS[neuron,time-1] >= v_thresh:
                SPIKE_TRAINS[neuron,time-1] = 0 
                SPIKE_TRAINS[neuron,time] = V_reset
                REFRACTORY_TIMES[neuron] = T_refract
                LAST_SPIKE[neuron] = time-1
            else:
                SPIKE_TRAINS[neuron,time] = SPIKE_TRAINS[neuron,time-1] + f(I_leak(SPIKE_TRAINS[neuron,time-1]), I_syn(neuron, SPIKE_TRAINS[neuron,time-1], time-1), I_ext=r(neuron))*dt

if __name__ == "__main__":
    simulate()
    fig, axs = plt.subplots(NR_OF_NEURONS)
    for i in range(NR_OF_NEURONS):
        axs[i].plot(t,SPIKE_TRAINS[i]) 
    plt.show()
