import numpy as np 
from ScalingTools import *
import matplotlib.pyplot as plt 
import random

class LeakyIntegrateAndFireNeuron:

    # Static attributes that are shared across all instances of this class
    # This should define the type of modelled neuron e.g. excitatory/inhibitory
    Tm = 20*ms
    El = -70*mV 
    # Rm = 10*bigMOhm
    # Ie = 3.1*nA
    RmIe = 18*mV
    thresholdPotential = -54*mV
    resetPotential = -80*mV

    # Synapse Parameters 
    Rmgs = 0.15
    maxs = 0.5
    Ts = 10*ms 
    Es = -0*mV 

    T = 1
    dt = 0.25*ms 
    t = np.linspace(0,T,int(T/dt)+1)

    def __init__(self, Id, siblings, conns, main_conn):
        # TODO Should contain all the neuron's it's connected to
        # Includes getting info from and getting info to
        self.id = Id 
        self.Psynapse = 0 
        self.spikeTrain = np.zeros(len(self.t))
        self.siblings = siblings
        self.v = 0 
        self.conns = conns 
        self.main_conn = main_conn

    def f(self, v, ps):
        return (self.El-v-self.Rmgs*ps*(v-self.Es)+self.RmIe)/self.Tm
    
    def p(self, ps):
        return -ps/self.Ts

    def simulate(self):
        # TODO get spike data from sibling neurons, if any 
        # using with and Lock to control access to resources 
        self.spikeTrain[0] = random.randrange(self.resetPotential/mV,self.thresholdPotential/mV)*mV
        # self.spikeTrain[0] = self.resetPotential
        for i in range(1,len(self.t)):

            # Send and receive past timestep voltage from coupled neuron 
            if self.id%2 == 0:
                self.v = self.conns.recv()
                self.conns.send(self.spikeTrain[i-1])
            else:
                self.conns.send(self.spikeTrain[i-1])
                self.v = self.conns.recv()
            
            # print(self.v)

            # With voltage from coupled neuron, if it's spiked increase synaptic weight 
            #   else decay with time constant 
            if self.v >= self.thresholdPotential:
                self.Psynapse += self.maxs
            else:
                self.Psynapse = self.Psynapse + self.p(self.Psynapse)*self.dt
            
            if self.spikeTrain[i-1] >= self.thresholdPotential:
                self.spikeTrain[i-1] = 0*mV
                self.spikeTrain[i] = self.resetPotential 
            else: 
                self.spikeTrain[i] = self.spikeTrain[i-1]+self.f(self.spikeTrain[i-1], self.Psynapse)*self.dt

        self.main_conn.send(self.spikeTrain)