import numpy as np
import matplotlib.pyplot as pl

class liaf:
  def __init__(self,
               time_constant=30.0,
               membrane_resistance=90.0,
               voltage_threshold=-50.0,
               voltage_reset=-65.0,
               equilibrium=-85.0,
               external_current=0.0):

   self.time_constant = time_constant
   self.membrane_resistance = membrane_resistance
   self.voltage_threshold = voltage_threshold
   self.voltage_reset = voltage_reset
   self.equilibrium = equilibrium
   self.external_current = external_current

   self.potential = self.voltage_reset

  def update_potential(self, initial_potential, t):
    if self.potential == 0.0:
      self.hyperpolarize()
    elif self.potential > self.voltage_threshold:
      self.generate_spike()
    else:
      self.potential = (self.equilibrium +
                       self.membrane_resistance * self.external_current +
                       np.exp(-t/self.time_constant) * (initial_potential -
                       self.equilibrium -
                       self.membrane_resistance * self.external_current))


  def hyperpolarize(self):
    self.potential = self.voltage_reset

  def generate_spike(self):
    self.potential = 0.0

  def simulate(self, time):
    # time is in milliseconds

    potentials = []
    currents = np.abs(np.sin(np.arange(time) + np.random.normal(size=[time])))
    for msec in range(time):
      self.external_current = currents[msec]
      self.update_potential(self.potential, 1)
      potentials.append(self.potential)


    plt.plot(range(time), potentials)

if __name__ == "__main__":
    neuron = liaf()
    neuron.simulate(100)
