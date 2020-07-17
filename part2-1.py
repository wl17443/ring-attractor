import numpy as np
import matplotlib.pyplot as plot
import decimal 
import random as rnd 

# Useful scaling tools 
ms = 0.001
mV = 0.001 
bigMOhm = 1000000
nA = 0.000000001
nS = 0.000000001

# Parameters in the integrate and fire model 
membraneTimeConstant = 10*ms 
leakyReversalPotential = -65*mV
resetPotential = leakyReversalPotential
membraneResistance = 100*bigMOhm
electrodeInputCurrent = (0)*nA
thresholdPotential = -50*mV
averageFiringRate = 15 

rmie = membraneResistance*electrodeInputCurrent

# Synapse parameters
gs = 4*nS
maxs = 0.5
synapseTimeConstant = 2*ms 
synapseReversalPotential = 0*mV
nrIncomingSynapses = 40

# range function but with floats 
def drange(x, y, jump):
  while x < y:
    yield float(x)
    x += decimal.Decimal(jump)

# Using euler's method to approximate spike-train 

# def sumofsynapseinput(v,ps):
#     total = 0
#     for i in range(len(ps)):
#         total += membraneResistance*ps[i]*gsynapses[i]*(v-synapseReversalPotential)
#     return total 

def synapsecurrent(v):
    output = []
    for i in range(nrIncomingSynapses):
        rmgspsves = gsynapses[i]*synapses[i]*membraneResistance*(v-synapseReversalPotential)
        output.append(rmgspsves)
    return sum(output)

def f(v):
    return (leakyReversalPotential-v-synapsecurrent(v)+rmie)/membraneTimeConstant

def p(ps):
    return -ps/synapseTimeConstant

## The initial condition 
v0 = resetPotential

## Timestep and total time 
dt = 0.25*ms
T = 1
t = np.linspace(0, T, int(T/dt)+1)
spike_train = np.zeros(len(t))
synapses = np.zeros(nrIncomingSynapses)
gsynapses = [gs]*nrIncomingSynapses

total_fires = 0 
spike_train[0] = v0
for i in range(1, len(t)):
    if spike_train[i-1] > thresholdPotential:
        total_fires += 1
        spike_train[i-1] = 0*mV
        spike_train[i] = resetPotential
    else:
        spike_train[i] = spike_train[i-1]+f(spike_train[i-1])*dt    

    # For each synapse, see if it fired an action potential in this time slice 
    for i in range(nrIncomingSynapses):
        if rnd.random() <= averageFiringRate*dt:
            synapses[i] += maxs
        else:
            synapses[i] = synapses[i]+p(synapses[i])*dt 

plot.title("Synapses with the Same Strengths (4 nS)")
plot.plot(t,spike_train)
plot.xlabel("Time (s)")
plot.ylabel("Voltage (V)")
plot.show()