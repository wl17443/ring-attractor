import numpy as np
import matplotlib.pyplot as plt
import random

# Useful scaling tools 
ms = 0.001
mV = 0.001 
bigMOhm = 1000000
nA = 0.000000001

# Parameters in the integrate and fire model 
membraneTimeConstant = 20*ms 
leakyReversalPotential = -70*mV
resetPotential = -80*mV
# membraneResistance = 10*bigMOhm
# electrodeInputCurrent = (3.1)*nA
rmie = 18*mV
thresholdPotential = -54*mV

# Synapse parameters
rmgs = 0.15
maxs = 0.5
synapseTimeConstant = 10*ms 
synapseReversalPotential = 0*mV

## Timestep and total time 
dt = 0.25*ms
T = 1
t = np.linspace(0, T, int(T/dt)+1)
spike_train1 = np.zeros(len(t))
spike_train2 = np.zeros(len(t))

v0 = random.randrange(resetPotential/mV,thresholdPotential/mV)
v1 = random.randrange(resetPotential/mV,thresholdPotential/mV)

def f(v,ps):
    return (leakyReversalPotential-v-rmgs*ps*(v-synapseReversalPotential)+rmie)/membraneTimeConstant

def p(ps):
    return -ps/synapseTimeConstant
    
spike_train1[0] = v0*mV
spike_train2[0] = v1*mV

Psynapse1 = 0
Psynapse2 = 0

for i in range(1,len(t)):
    if spike_train1[i-1] > thresholdPotential:
        Psynapse2 += maxs 
    else: 
        Psynapse2 = Psynapse2 + p(Psynapse2)*dt 

    if spike_train2[i-1] > thresholdPotential:
        Psynapse1 += maxs 
    else: 
        Psynapse1 = Psynapse1+p(Psynapse1)*dt

    if spike_train1[i-1] > thresholdPotential:
        spike_train1[i-1] = 0*mV
        spike_train1[i] = resetPotential
    else:
        spike_train1[i] = spike_train1[i-1]+f(spike_train1[i-1],Psynapse1)*dt
    

    if spike_train2[i-1] > thresholdPotential:
        spike_train2[i-1] = 0*mV
        spike_train2[i] = resetPotential
    else:
        spike_train2[i] = spike_train2[i-1]+f(spike_train2[i-1],Psynapse2)*dt


fig, ax = plt.subplots(3,1)
ax[0].plot(t, spike_train1)
ax[1].plot(t, spike_train2)
ax[2].plot(t, spike_train1)
ax[2].plot(t, spike_train2)
plt.show()
