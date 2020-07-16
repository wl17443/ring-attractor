import numpy as np
import matplotlib.pyplot as plot
import decimal 

# Useful scaling tools 
ms = 0.001
mV = 0.001 
bigMOhm = 1000000
nA = 0.000000001

# Parameters in the integrate and fire model 
membraneTimeConstant = 10*ms 
leakyReversalPotential = -70*mV
resetPotential = -70*mV
membraneResistance = 10*bigMOhm
electrodeInputCurrent = 3.1*nA
thresholdPotential = -49*mV

# Using euler's method to approximate spike-train 
def f(v):
    return (leakyReversalPotential-v+membraneResistance*electrodeInputCurrent)/membraneTimeConstant

## The initial condition 
v0 = resetPotential

## Timestep and total time 
dt = 0.25*ms
T = 1
t = np.linspace(0, T, int(T/dt)+1)
spike_train = np.zeros(len(t))

def simulate():
    spike_train[0] = v0
    for i in range(1, len(t)):
        spike_train[i] = spike_train[i-1]+f(spike_train[i-1])*dt
        if spike_train[i-1] >= thresholdPotential:
            spike_train[i-1] = 0
            spike_train[i] = resetPotential 

simulate()
plot.figure()
plot.plot(t, spike_train)
plot.show()
plot.savefig('spike_train.png')

