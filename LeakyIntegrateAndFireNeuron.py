import numpy as np 
from ScalingTools import *
import matplotlib.pyplot as plt 
import random
from Dictionaries import *

class LeakyIntegrateAndFireNeuron:

    # Synapse Parameters 
    Rmgs = 0.15
    maxs = 0.5
    Ts = 10*ms 

    # Static attributes that are shared across all LIAF neurons
    T = 1
    dt = 0.25*ms 
    t = np.linspace(0,T,int(T/dt)+1)

    def __init__(self, Id, neurontype, neuron_params, to_siblings_conns, from_siblings_conns, main_conn):
        self.id = Id 
        # Multiple synaptic weights 
        self.Psynapses = np.zeros(len(from_siblings_conns))

        # Initialise neuron spike train to 0*len(t)
        self.spikeTrain = np.zeros(len(self.t))

        # Define number of connecting neurons respective of their direction 
        self.to_siblings_conns = to_siblings_conns 
        self.from_siblings_conns = from_siblings_conns
        self.to_siblings = len(to_siblings_conns)
        self.from_siblings = len(from_siblings_conns)

        # Define connection to mother neuron
        self.main_conn = main_conn

        # Multiple presynaptic fires 
        # Get 1 for fired and 0 for not fired from coupled neuron(s)
        self.fire_signals = np.zeros(len(from_siblings_conns))

        # Neuron parameters defined by neuron type and other user inputs 
        self.Es = neuronType[neurontype]
        self.neuron_params = neuron_params

    def f(self, v):
        return (self.neuron_params['El']-v-(self.Rmgs*self.Psynapses*(v-self.Es)).sum()+self.neuron_params['RmIe'])/self.neuron_params['Tm']
    
    def p(self, ps):
        return -ps/self.Ts

    def simulate(self):
        # Randomly choose a starting membrane potential 
        self.spikeTrain[0] = random.randrange(self.neuron_params['resetPotential']/mV,self.neuron_params['thresholdPotential']/mV)*mV
        # Get spike data from sibling neurons, if any 
        for i in range(1,len(self.t)):
            # Send and receive spiked (boolean) from coupled neuron(s)
            # Even neurons send first then receive 
            if self.id%2==0:
                if self.to_siblings > 0:
                    for to_sibling in self.to_siblings_conns:
                        to_sibling.send(self.spikeTrain[i-1]>=self.neuron_params['thresholdPotential'])
                # for from_sibling in self.from_siblings_conns:
                #     self.fire_signals[from_sibling] = from_sibling.recv()
                if self.from_siblings > 0:
                    for from_sibling_nr in range(self.from_siblings):
                        self.fire_signals[from_sibling_nr] = self.from_siblings_conns[from_sibling_nr].recv()
            else:
                if self.from_siblings > 0:
                    for from_sibling_nr in range(self.from_siblings):
                        self.fire_signals[from_sibling_nr] = self.from_siblings_conns[from_sibling_nr].recv()
                if self.to_siblings > 0:
                    for to_sibling in self.to_siblings_conns:
                        to_sibling.send(self.spikeTrain[i-1]>=self.neuron_params['thresholdPotential'])
        
            # With voltage from coupled neuron, if it's spiked increase synaptic weight 
            #   else decay with time constant
            if self.from_siblings > 0:
                for sibling in range(self.from_siblings):
                    if self.fire_signals[sibling]:
                        self.Psynapses[sibling] += self.maxs
                    else:
                        self.Psynapses[sibling] = self.Psynapses[sibling] + self.p(self.Psynapses[sibling])*self.dt
                
            # Using Euler's method, calculate the current membrane potential 
            if self.spikeTrain[i-1] >= self.neuron_params['thresholdPotential']:
                self.spikeTrain[i-1] = 0*mV
                self.spikeTrain[i] = self.neuron_params['resetPotential'] 
            else: 
                self.spikeTrain[i] = self.spikeTrain[i-1]+self.f(self.spikeTrain[i-1])*self.dt

        # Upon simulation complete, send spike train to mother process 
        self.main_conn.send(self.spikeTrain)