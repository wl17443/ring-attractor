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
electrodeInputCurrent = 0*nA
thresholdPotential = -50*mV

rmie = membraneResistance*electrodeInputCurrent

# Synapse parameters
gs = 4*nS
maxs = 0.5
synapseTimeConstant = 2*ms 
synapseReversalPotential = 0*mV
nrIncomingSynapses = 40

# STDP parameters 
STDP = True 
aplus = 0.2*nS
aminus = 0.25*nS 
plusTimeConstant = 20*ms
minusTimeConstant = 20*ms 

## The initial condition 
v0 = resetPotential

## Parameters to simulate postsynapse voltage 
dt = 0.25*ms
T = 300 
t = np.linspace(0, T, int(T/dt)+1)
# spike_train2 = np.zeros(len(t))

# Simulate 40 spike trains as poisson processes 
presynapseSpikeTrains = np.zeros([len(t),40])
presynapsestats = np.zeros([40,3])
postsynapseSpikeTime = -1000*ms

# randomnumbers = np.random.random([len(t),40])

def initialize_synapse_stats():
    for i in range(40):
        presynapsestats[i,0] = gs


def synapsecurrent(v):
    output =  0
    for i in range(nrIncomingSynapses):
        rmgspsves = presynapsestats[i,0]*presynapsestats[i,1]*membraneResistance*(v-synapseReversalPotential)
        output += rmgspsves
    return output

def f(v):
    return (leakyReversalPotential-v-synapsecurrent(v)+rmie)/membraneTimeConstant

def p(ps):
    return -ps/synapseTimeConstant

def stdp(t):
    if t > 0:
        return aplus*np.exp(-np.abs(t)/plusTimeConstant)
    else:
        return -aminus*np.exp(-np.abs(t)/minusTimeConstant)

B = 20
freq = 10 
r0 = 20

def r(t): 
    return r0 + B*np.sin(2*np.pi*freq*t)


def simulate(presynapseSpikeTrains,presynapsestats,postsynapseSpikeTime, spike_train, spike_train2, averageFiringRate, STDP): 
    # firing_rate = 0
    # steady_state_gsynapse = np.zeros(40)
    for i in range(1, len(t)):
        for j in range(40):
            # firing_rate = firing_rate+dt*r(i-1)
            # if rnd.random() < r((i-1)*dt)*dt:
            if rnd.random() < averageFiringRate*dt:
                presynapsestats[j,2] = (i-1)*dt
                presynapsestats[j,1] += maxs 
                if STDP:
                    presynapsestats[j,0] += stdp(postsynapseSpikeTime-(i-1)*dt)
                    if presynapsestats[j,0] > 4*nS:
                        presynapsestats[j,0] = 4*nS
                    elif presynapsestats[j,0] < 0:
                        presynapsestats[j,0] = 0 
            else:
                presynapsestats[j,1] = presynapsestats[j,1] + p(presynapsestats[j,1])*dt 
        if spike_train[i-1] > thresholdPotential:
            postsynapseSpikeTime = (i-1)*dt
            spike_train[i-1] = 0*mV
            spike_train[i] = resetPotential
            spike_train2[i-1] = 1
            if STDP and presynapseSpikeTrains[i-1,j] == 0:
                for j in range(40):
                    presynapsestats[j,0] += stdp(postsynapseSpikeTime-presynapsestats[j,2])
                    if presynapsestats[j,0] > 4*nS:
                        presynapsestats[j,0] = 4*nS
                    elif presynapsestats[j,0] < 0:
                        presynapsestats[j,0] = 0 
        else:
            spike_train[i] = spike_train[i-1]+f(spike_train[i-1])*dt    

    # for x in range(40):
    #     steady_state_gsynapse[x] = presynapsestats[x,0] 
    
    # return steady_state_gsynapse

STDP = False 
# steady_state_gsynapses = []
# for x in range(0,21,5):
#     B = x
#     print(B)
# averageFiringRate = 0
# B=0 
# spike_train = np.zeros(len(t))
# initialize_synapse_stats()
# result = simulate(presynapseSpikeTrains,presynapsestats,postsynapseSpikeTime,spike_train, STDP)
# steady_state_gsynapses.append(result)

# B=20
STDP = True 
spike_trains = []
for i in range(10,21):
    spike_train = np.zeros(len(t))
    spike_train2 = np.zeros(len(t))
    initialize_synapse_stats()
    simulate(presynapseSpikeTrains,presynapsestats,postsynapseSpikeTime,spike_train, spike_train2, i, STDP)
    spike_trains.append(spike_train2)


# np.savetxt('gsynapses.csv', steady_state_gsynapses, delimiter=', ')

# def test_firing_rate():
#     firing_rate = []
#     for i in range(len(t)):
#         firing_rate.append(r((i-1)*dt))
#     return firing_rate

# result = test_firing_rate()
# plot.plot(t,result)
np.savetxt('spike_train.csv',spike_trains,delimiter=', ')
# plot.show()
