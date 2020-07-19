# Leaky integrate and fire model
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

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
    Pmax = 1.0
    synapticTimeConstant = 17.0 * ms
    openChannelP = 0.0

    def __init__(self, leaky=True, excitatory=True):
        if not leaky:
            self.leakyReversalPotential = 0.0

        if not excitatory:
            self.synapticReversalPotential = -80.0 * mV


    def step(self):
        self._hyperpolarize()

        self._updateOpenChannelP()
        self._updatePotential()
        self._depolarize()

        self.timeFromSpike += 1.0 * ms


    def receiveActionPotential(self):
        self.timeFromSpike = 0.0 * ms


    def _updateOpenChannelP(self):
        self.openChannelP =  self.Pmax / self.synapticTimeConstant * self.timeFromSpike * np.exp(1.0 - self.timeFromSpike / self.synapticTimeConstant)

    def _updatePotential(self):
        self.potential += (self.leakyReversalPotential 
                           - self.potential 
                           - 0.05 * self.openChannelP * (self.potential - self.synapticReversalPotential) 
                           + self.membraneResistance * self.electrodeInputCurrent) / self.membraneTimeConstant * ms

    def _hyperpolarize(self):
        if self.potential == 0.0:
            self.potential = self.resetPotential

    def _depolarize(self):
        if self.potential >= self.thresholdPotential:
            self.potential = 0.0




if __name__ == "__main__":
    time = 100
    neurons = [lif() for _ in range(2)]

    potentials = [[], []]
    for t in range(time):
        for i, neuron in enumerate(neurons):
            neurons[0].electrodeInputCurrent = 2.5* nA
            if t > 0:
                neurons[1].electrodeInputCurrent = 2.5* nA


            neuron.step()

            if neuron.potential == 0.0:
                neurons[1 - i].receiveActionPotential()

            potentials[i].append(neuron.potential)

    fig, axes = plt.subplots(3, 1, figsize=(12, 10))
    axes[0].plot(range(time), potentials[0])
    axes[0].set_title("Voltage of first neuron")
    # sns.lineplot(range(time), potentials[0], ax=axes[0])
    # sns.lineplot(range(time), potentials[1], ax=axes[1])


    axes[1].plot(range(time), potentials[1])
    axes[1].set_title("Voltage of second neuron")

    axes[2].plot(range(time), potentials[0])
    axes[2].plot(range(time), potentials[1])
    axes[2].set_title("Voltages of both neurons overlapped")
    axes[2].set_xlabel("Time (ms)")

    for ax in axes:
        ax.set_ylabel("Voltage (mV)")

    plt.show()
