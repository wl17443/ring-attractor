import numpy as np
import matplotlib.pyplot as plt

def euler(f, y0, tot_time):
        t, y = 0, y0
    
        solutions = [y]
        while t <= tot_time:
            if y == 0.0:
                y = -65.0

            t += 1
            y += f(t,y)

            if y > -50.0:
                y = 0.0

            solutions.append(y)
        return solutions


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

    
    def voltage(self, time, old_voltage):
        v_t = (self.equilibrium - old_voltage + self.membrane_resistance*self.external_current) / self.time_constant
        return v_t



    def simulate(self, time):
        # time is in milliseconds
        self.external_current = 0.5
        potentials = euler(self.voltage, self.voltage_reset, time)

        plt.plot(range(time+2), potentials)
        plt.show()

if __name__ == "__main__":
    neuron = liaf()
    neuron.simulate(100)
