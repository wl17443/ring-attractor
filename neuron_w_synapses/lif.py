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
    synapticReversalPotential = 0.0 * mV
    resetPotential = -80.0 * mV
    membraneResistance = 10.0 * bigMOhm
    electrodeInputCurrent = 0.0 * nA
    thresholdPotential = -54.0 * mV

    potential = resetPotential
    synapticCurrent = 0.0
    timeFromSpike = 10.0 * ms
    ocp = 0.0

    def updatePotential(self):
        if self.potential == 0.0:
            self.potential = self.resetPotential

        self.timeFromSpike += 1.0 * ms
        leakage = self.leakyReversalPotential - self.potential
        externalCurrent = self.membraneResistance * self.electrodeInputCurrent
        self.synapticCurrent = - 0.05 * self.openChannelP() * (self.potential -
                                                              self.synapticReversalPotential)

        self.potential += (leakage + externalCurrent +
                           self.synapticCurrent) / self.membraneTimeConstant * ms

        if self.potential >= self.thresholdPotential:
            self.potential = 0.0

        self.ocp = self.openChannelP()

    def openChannelP(self):
        Pmax = 1.0
        timeConstant = 17.0 * ms
        return Pmax / timeConstant * self.timeFromSpike * np.exp(1.0 - self.timeFromSpike / timeConstant)


if __name__ == "__main__":
    time = 150
    neurons = [lif() for _ in range(2)]

    potentials = [[], []]
    synapticCurrents = [[], []]
    ocps = [[], []]
    for t in range(time):
        for i, neuron in enumerate(neurons):
            neurons[0].electrodeInputCurrent = 2.5* nA
            if t > 0:
                neurons[1].electrodeInputCurrent = 2.5* nA


            neuron.updatePotential()

            if neuron.potential == 0.0:
                neurons[1 - i].timeFromSpike = 0.0

            potentials[i].append(neuron.potential)
            synapticCurrents[i].append(neuron.synapticCurrent)
            ocps[i].append(neuron.ocp)

    fig, ax = plt.subplots(3, 2, figsize=(10, 10))
    ax[0, 0].plot(range(time), potentials[0])
    ax[0, 0].set_title("Potentials of neuron 1")

    ax[0, 0].plot(range(time), potentials[1], color="g")

    ax[1, 0].plot(range(time), potentials[1])
    ax[1, 0].set_title("Potentials of neuron 2")

    ax[0, 1].plot(range(time), synapticCurrents[0])
    ax[0, 1].set_title("Synaptic current of neuron 1")

    ax[1, 1].plot(range(time), synapticCurrents[1])
    ax[1, 1].set_title("Synaptic current of neuron 2")

    ax[2, 0].plot(range(time), ocps[0])
    ax[2, 0].set_title("Open channel probability 1")

    ax[2, 1].plot(range(time), ocps[1])
    ax[2, 1].set_title("Open channel probability 2")

    plt.show()
