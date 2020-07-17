# Leaky integrate and fire model

import numpy as np
import matplotlib.pyplot as plt

ms = 0.001
mV = 0.001
bigMOhm = 1000000
nA = 0.000000001 

class lif:
    def __init__(self,
            membraneTimeConstant = 10*ms,
            leakyReversalPotential = -75*mV,
            resetPotential = -65*mV,
            membraneResistance = 10*bigMOhm,
            electrodeInputCurrent = 0*nA,
            thresholdPotential = -50*mV):

        self.membraneTimeConstant = membraneTimeConstant
        self.leakyReversalPotential = leakyReversalPotential
        self.resetPotential = resetPotential
        self.membraneResistance = membraneResistance
        self.electrodeInputCurrent = electrodeInputCurrent
        self.thresholdPotential = thresholdPotential
 
        self.potential = self.resetPotential

    def updatePotential(self):

        # Depolarize after spike
        if self.potential == 0.0:
            self.potential = self.resetPotential

        # Update membrane potential
        self.potential += ((self.leakyReversalPotential - self.potential + self.membraneResistance*self.electrodeInputCurrent) / self.membraneTimeConstant) * ms

        # Spiking mechanism
        if self.potential >= self.thresholdPotential:
            self.potential = 0.0


class electrode:
    def __init__(self, fun=None, const=None):
        self.fun = fun
        self.const = const

        self.outSynapses = {}

    def connect(self, neuron, weight=1.0):
        self.outSynapses[neuron] = weight

    def simulate(self, time):
        recording = []
        for t in range(time):
            for neuron, weight in self.outSynapses.items():
                neuron.electrodeInputCurrent = self.output(time) * weight
                neuron.updatePotential()
                recording.append(neuron.potential)

        return recording

    def output(self, time=-1):
        if self.const:
            return self.const

        if self.fun:
            assert time > -1
            return self.fun(time)



if __name__ == "__main__":
    fun = lambda time: np.abs(np.sin(time)*3.1 + np.random.normal())*nA
    time = 1000
    neuron = lif()
    electrode = electrode(const=3.1*nA)
    # electrode = electrode(fun=fun)
    electrode.connect(neuron)
    potentials = electrode.simulate(time)


    plt.plot(range(time), potentials)
    plt.show()