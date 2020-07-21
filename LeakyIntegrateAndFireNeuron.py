import numpy as np 
from ScalingTools import *
import matplotlib.pyplot as plt 
import random

neuronType = {
    "i": -80*mV,
    "e": 0*mV
}

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
    # Es = -80*mV 

    T = 1
    dt = 0.25*ms 
    t = np.linspace(0,T,int(T/dt)+1)

    def __init__(self, Id, neurontype, siblings, sibling_conns, main_conn):
        # TODO Should contain all the neuron's it's connected to
        # Includes getting info from and getting info to
        self.id = Id 
        # TODO multiple synaptic weights 
        self.Psynapses = np.zeros(len(siblings))
        self.spikeTrain = np.zeros(len(self.t))
        self.siblings = siblings
        self.sibling_conns = sibling_conns 
        self.main_conn = main_conn
        # TODO multiple presynaptic voltages 
        # Get 1 for fired and 0 for not fired from coupled neuron(s)
        self.fire_signals = np.zeros(len(siblings))
        self.Es = neuronType[neurontype]
        # TODO add output neuron (boolean) parameter 
        # TODO add layer number as parameter (?)

    def f(self, v, ps):
        return (self.El-v-self.Rmgs*ps*(v-self.Es)+self.RmIe)/self.Tm
    
    def p(self, ps):
        return -ps/self.Ts

    def simulate(self):
        # Randomly choose a starting membrane potential 
        self.spikeTrain[0] = random.randrange(self.resetPotential/mV,self.thresholdPotential/mV)*mV
        # Get spike data from sibling neurons, if any 
        for i in range(1,len(self.t)):
            # Send and receive spiked (boolean) from coupled neuron(s)
            for sibling in range(len(self.siblings)):
                if self.id%2 == 0:
                    self.fire_signals[sibling] = self.sibling_conns.recv()
                    self.sibling_conns.send(self.spikeTrain[i-1]>=self.thresholdPotential)
                else:
                    self.sibling_conns.send(self.spikeTrain[i-1]>=self.thresholdPotential)
                    self.fire_signals[sibling] = self.sibling_conns.recv()

            # With voltage from coupled neuron, if it's spiked increase synaptic weight 
            #   else decay with time constant
            for sibling in range(len(self.siblings)):
                if self.fire_signals[sibling]:
                    self.Psynapses[sibling] += self.maxs
                else:
                    self.Psynapses[sibling] = self.Psynapses[sibling] + self.p(self.Psynapses[sibling])*self.dt
                
            # Using Euler's method, calculate the current membrane potential 
            if self.spikeTrain[i-1] >= self.thresholdPotential:
                self.spikeTrain[i-1] = 0*mV
                self.spikeTrain[i] = self.resetPotential 
            else: 
                self.spikeTrain[i] = self.spikeTrain[i-1]+self.f(self.spikeTrain[i-1], self.Psynapses)*self.dt

        # Upon simulation complete, send spike train to mother process 
        self.main_conn.send(self.spikeTrain)