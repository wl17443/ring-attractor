import numpy as np
import matplotlib.pyplot as plt

ms = 0.001
mV = 0.001
bigMOhm = 1000000
nA = 0.000000001 

# Parameters in the integrate and fire model

class liaf:
    def __init__(self,
            membraneTimeConstant = 30*ms,
            leakyReversalPotential = -85*mV,
            resetPotential = -65*mV,
            membraneResistance = 90*bigMOhm,
            electrodeInputCurrent = 0*nA,
            thresholdPotential = -50*mV):

        self.membraneTimeConstant = membraneTimeConstant
        self.leakyReversalPotential = leakyReversalPotential
        self.resetPotential = resetPotential
        self.membraneResistance = membraneResistance
        self.electrodeInputCurrent = electrodeInputCurrent
        self.thresholdPotential = thresholdPotential
 
        self.potential = self.resetPotential

    def updatePotential(self, initialPotential, t):
        if self.potential == 0.0:
            self.hyperpolarize()
        elif self.potential > self.thresholdPotential:
            self.generate_spike()
        else:
            self.potential = (self.leakyReversalPotential +
                    self.membraneResistance * self.electrodeInputCurrent +
                    np.exp(-t/self.membraneTimeConstant) * (initialPotential -
                        self.leakyReversalPotential -
                        self.membraneResistance * self.electrodeInputCurrent))


    def hyperpolarize(self):
        self.potential = self.resetPotential

    def generate_spike(self):
        self.potential = 0.0

    def simulate(self, time, steps):
        # time is in milliseconds

        potentials = [self.resetPotential]
        timesteps = np.linspace(0, time, num=steps)
        currents = np.abs(np.sin(np.arange(len(timesteps)) + np.random.normal(size=[len(timesteps)])))*nA

        for i, step in enumerate(np.diff(timesteps)):
            self.electrodeInputCurrent = currents[i]
            self.updatePotential(self.potential, step)
            potentials.append(self.potential)


        plt.plot(timesteps, potentials)
        plt.show()

if __name__ == "__main__":
    neuron = liaf()
    neuron.simulate(1, 200)
