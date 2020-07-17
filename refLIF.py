# Leaky integrate and fire model with Spike Rate Adaptation (Refractoriness)
import numpy as np
import matplotlib.pyplot as plt

ms = 0.001
mV = 0.001
bigMOhm = 1000000
nA = 0.000000001 

class refLIF:
    def __init__(self,
            membraneTimeConstant = 10*ms,
            leakyReversalPotential = -75*mV,
            resetPotential = -65*mV,
            membraneResistance = 10*bigMOhm,
            electrodeInputCurrent = 0*nA,
            thresholdPotential = -50*mV,

            # Spike Rate Adaptation Stuff
            spikeRateAdaptationDelta = 0.6, # How much to increase SRA after every spike
            spikeRateAdaptationTimeConstant = 100*ms, # How fast SRA decays
            potassiumReversalPotential = -70*mV): # Were is the equilibrium point of SRA 

        self.membraneTimeConstant = membraneTimeConstant
        self.leakyReversalPotential = leakyReversalPotential
        self.resetPotential = resetPotential
        self.membraneResistance = membraneResistance
        self.electrodeInputCurrent = electrodeInputCurrent
        self.thresholdPotential = thresholdPotential
 
        # Spike Rate Adaptation Stuff
        self.potassiumReversalPotential = potassiumReversalPotential
        self.spikeRateAdaptationDelta = spikeRateAdaptationDelta 
        self.spikeRateAdaptationTimeConstant = spikeRateAdaptationTimeConstant
        self.spikeRateAdaptationConductance = 0.0

        self.potential = self.resetPotential

    def updatePotential(self):

        # Depolarize after spike
        if self.potential == 0.0:
            self.potential = self.resetPotential

        # Update membrane potential
        # TODO Check the formula for spike rate adaptation, may be missing some resistance
        self.potential += ((self.leakyReversalPotential - self.potential - self.spikeRateAdaptationConductance * (self.potential - self.potassiumReversalPotential) + self.membraneResistance*self.electrodeInputCurrent) / self.membraneTimeConstant) * ms

        # Update spike rate adaptation conductance
        self.spikeRateAdaptationConductance -= self.spikeRateAdaptationConductance/self.spikeRateAdaptationTimeConstant*ms

        # Spiking mechanism
        if self.potential >= self.thresholdPotential:
            self.potential = 0.0
            self.spikeRateAdaptationConductance += self.spikeRateAdaptationDelta


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
    neuron = refLIF()
    electrode = electrode(const=3.1*nA)
    # electrode = electrode(fun=fun)
    electrode.connect(neuron)
    potentials = electrode.simulate(time)


    plt.plot(range(time), potentials)
    plt.show()
