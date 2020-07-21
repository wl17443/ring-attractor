import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint


uA = 0.000001 
uF = 0.000001
mS = ms = mV = 0.001
bigMOhm = 1000000
cm2 = 0.01 ** 2


class hh:
    membraneCapacitance = 1.0 * uF/cm2

    leakageConductance = 0.3 * mS/cm2
    potassiumConductance = 36.0 * mS/cm2
    sodiumConductance = 120.0 * mS/cm2

    leakyReversalPotential = -54.387 * mV
    potassiumReversalPotential = -77.0 * mV
    sodiumReversalPotential = 50.0 * mV

    electrodeInputCurrent = 35 * uA/cm2

    initialValues = [-65 * mV, 0.05, 0.6, 0.32]
    t = np.linspace(0.0, 100.0, 1000)


    def simulate(self):
        X = odeint(self.update, self.initialValues, self.t, args=(self,))
        V = X[:,0]
        m = X[:,1]
        h = X[:,2]
        n = X[:,3]

        fig, ax = plt.subplots(2, 2, figsize=(10, 10))
        ax[0,0].plot(self.t, V)
        ax[0,0].set_title("V")

        ax[0,1].plot(self.t, n)
        ax[0,1].set_title("n")
        
        ax[1,0].plot(self.t, m)
        ax[1,0].set_title("m")

        ax[1,1].plot(self.t, h)
        ax[1,1].set_title("h")
        plt.show()
        

    @staticmethod
    def update(X, t, self):
        V, m, h, n = X

        dV = (self.electrodeInputCurrent - self.sodiumCurrent(V, m, h) - self.potassiumCurrent(V, n) - self.leakageCurrent(V)) / self.membraneCapacitance

        dn = self.alpha_n(V)*(1.0-n) - self.beta_n(V)*n
        dm = self.alpha_m(V)*(1.0-m) - self.beta_m(V)*m
        dh = self.alpha_h(V)*(1.0-h) - self.beta_h(V)*h

        return dV, dm, dh, dn


    def leakageCurrent(self, V):
        return self.leakageConductance * (V - self.leakyReversalPotential)

    def potassiumCurrent(self, V, n):
        return self.potassiumConductance  * n**4 * (V - self.potassiumReversalPotential)

    def sodiumCurrent(self, V, m, h):
        return self.sodiumConductance * m**3 * h * (V - self.sodiumReversalPotential)

    def alpha_m(self, V):
        return 0.1*(V+40.0)/(1.0 - np.exp(-(V+40.0) / 10.0))

    def beta_m(self, V):
        return 4.0*np.exp(-(V+65.0) / 18.0)

    def alpha_h(self, V):
        return 0.07*np.exp(-(V+65.0) / 20.0)

    def beta_h(self, V):
        return 1.0/(1.0 + np.exp(-(V+35.0) / 10.0))

    def alpha_n(self, V):
        return 0.01*(V+55.0)/(1.0 - np.exp(-(V+55.0) / 10.0))

    def beta_n(self, V):
        return 0.125*np.exp(-(V+65) / 80.0)


if __name__ == "__main__":
    neuron = hh()
    neuron.simulate()
