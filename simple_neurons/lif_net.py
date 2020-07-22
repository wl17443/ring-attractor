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

    def __init__(self):
        self.synapticCurrent = 0.0
        self.timeFromExSpike = 100.0 * ms
        self.timeFromInSpike = 100.0 * ms
        self.openExChannelP = 0.0
        self.openInChannelP = 0.0
        self.synapses = {"excitatory": [], "inhibitory": []}

        self.potential = self.resetPotential





    def step(self):
        self._hyperpolarize()

        self._updateOpenExChannelP()
        self._updateOpenInChannelP()
        self._updatePotential()
        self._depolarize()

        self.timeFromExSpike += 1.0 * ms
        self.timeFromInSpike += 1.0 * ms

    def makeSynapse(self, target, kind):
        self.synapses[kind].append(target)

    def receiveActionPotential(self, kind):
        if kind == "excitatory":
            self.timeFromExSpike = 0.0 * ms

        if kind == "inhibitory":
            self.timeFromInSpike = 0.0 * ms

    def _updatePotential(self):
        self.potential += (
            self.leakyReversalPotential - self.potential

            - 0.15 * self.openExChannelP *
            (self.potential - self.exSynapticReversalPotential)
            - 0.15 * self.openInChannelP *
            (self.potential - self.inSynapticReversalPotential)

            + self.membraneResistance * self.electrodeInputCurrent) / self.membraneTimeConstant * ms

    def _hyperpolarize(self):
        if self.potential == 0.0:
            self.potential = self.resetPotential

    def _depolarize(self):
        if self.potential >= self.thresholdPotential:
            self.potential = 0.0
            self._sendSpikes()

    def _sendSpikes(self):
        for neuron in self.synapses["excitatory"]:
            neuron.receiveActionPotential("excitatory")

        for neuron in self.synapses["inhibitory"]:
            neuron.receiveActionPotential("inhibitory")

    def _updateOpenExChannelP(self):
        # self.openExChannelP = self.Pmax / self.synapticTimeConstant * self.timeFromExSpike * \
        #     np.exp(1.0 - self.timeFromExSpike / self.synapticTimeConstant)
        self.openExChannelP = - self.openExChannelP / self.synapticTimeConstant * ms
        if self.timeFromExSpike == 0.0:
            self.openExChannelP += self.Pmax

    def _updateOpenInChannelP(self):
        # self.openInChannelP = self.Pmax / self.synapticTimeConstant * self.timeFromInSpike * \
        #     np.exp(1.0 - self.timeFromInSpike / self.synapticTimeConstant)
        self.openInChannelP = - self.openInChannelP / self.synapticTimeConstant * ms
        if self.timeFromInSpike == 0.0:
            self.openInChannelP += self.Pmax


