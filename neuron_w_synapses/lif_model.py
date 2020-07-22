# Leaky integrate and fire model
import numpy as np
import matplotlib.pyplot as plt

ms = 0.001
mV = 0.001
bigMOhm = 1000000
nA = 0.000000001


class lif:
    membraneTimeConstant = 20.0 * ms
    leakyReversalPotential = -70.0 * mV
    exSynapticReversalPotential = 0.0 * mV
    inSynapticReversalPotential = -80.0 * mV
    resetPotential = -80.0 * mV
    membraneResistance = 10.0 * bigMOhm
    electrodeInputCurrent = 0.0 * nA
    thresholdPotential = -54.0 * mV
    synapticTimeConstant = 10.0 * ms
    Pmax = 0.5

    def __init__(self, ID):
        self.id = ID
        self.synapticCurrent = 0.0
        self.synapses = {} # neuron: weight

        self.potential = self.resetPotential


    def step(self):
        self._hyperpolarize()

        self._updateSynapticCurrent()
        self._updatePotential()
        self._depolarize()

    def _updateSynapticCurrent(self):
        self.synapticCurrent = 0.0

        for neuron, weight in self.synapses.items():
            if neuron.potential == 0.0:
                self.synapticCurrent += weight
            

    def _updatePotential(self):
        self.potential += (
            self.leakyReversalPotential - self.potential
            + self.synapticCurrent * self.membraneTimeConstant
            + self.membraneResistance * self.electrodeInputCurrent) / self.membraneTimeConstant * ms

    def _hyperpolarize(self):
        if self.potential == 0.0:
            self.potential = self.resetPotential

    def _depolarize(self):
        if self.potential >= self.thresholdPotential:
            self.potential = 0.0

