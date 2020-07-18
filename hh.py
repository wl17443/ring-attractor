# Leaky integrate and fire model

import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint

nA = 0.000000001 
uF = 0.000001
mS = ms = mV = mm = 0.001
bigMOhm = 1000000

class hh:
    def __init__(self,
            membraneCapacitance = 0.01 * uF/(mm**2), # Check if right

            leakageConductance = 0.003 * mS/(mm**2),
            potassiumConductance = 0.36 * mS/(mm**2),
            sodiumConductance =  1.2 * mS/(mm**2),

            leakyReversalPotential = -54.387*mV,
            potassiumReversalPotential = -77.0*mV,
            sodiumReversalPotential = 50.0*mV,

            electrodeInputCurrent = 0*nA,
            initialN = 0.32,
            initialM = 0.05,
            initialH = 0.6,
            initialV = -65*mV):


        self.membraneCapacitance = membraneCapacitance

        self.leakageConductance = leakageConductance
        self.potassiumConductance = potassiumConductance
        self.sodiumConductance = sodiumConductance

        self.leakyReversalPotential = leakyReversalPotential
        self.potassiumReversalPotential = potassiumReversalPotential
        self.sodiumReversalPotential = sodiumReversalPotential

        self.electrodeInputCurrent = 3.5*nA/(mm**2)
        self.t = np.arange(0.0, 450.0, 0.01)


        self.n = initialN
        self.m = initialM
        self.h = initialH
        self.V = initialV


    @staticmethod
    def updatePotential(X, t, self):
        V, m, h, n = X

        dv = (-self.leakageCurrent() - self.potassiumCurrent() - self.sodiumCurrent() + self.electrodeInputCurrent) / self.membraneCapacitance
        dn = self.openingRateK()*(1.0 - self.n) - self.closingRateK() * self.n
        dm = self.openingRateActivationNa()*(1.0 - self.m) - self.closingRateActivationNa() * self.m
        dh = self.openingRateInactivationNa()*(1.0 - self.h) - self.closingRateActivationNa() * self.h

        return dv, dn, dm, dh

    def leakageCurrent(self):
        return self.leakageConductance * (self.V - self.leakyReversalPotential)

    def potassiumCurrent(self):
        return self.potassiumConductance * (self.n ** 4) * (self.V - self.potassiumReversalPotential)

    def sodiumCurrent(self):
        return self.sodiumConductance * self.h * (self.m ** 3) * (self.V - self.sodiumReversalPotential) 


    def openingRateK(self):
        # return 0.01 * (10 - self.V) / (np.exp((10 - self.V) / 10) - 1)
        return 0.01 * (55.0 + self.V) / (1.0 - np.exp(-(55.0 + self.V) / 10.0))

    def closingRateK(self):
        # return 0.125 * np.exp(-self.V / 80.0)
        return 0.125 * np.exp(-(self.V + 65.0) / 80.0)

    def openingRateActivationNa(self):
        return 0.1*(self.V + 40.0) / (1.0 - np.exp(-(self.V+40.0) / 10.0))
        # return 0.1 * (25 - self.V) / (np.exp((25 - self.V) / 10) -1)

    def closingRateActivationNa(self):
        # return 4.0 * np.exp(-self.V / 18.0)
        return 4.0 * np.exp(-(self.V + 65.0) / 18.0)

    def openingRateInactivationNa(self):
        # return 0.07 * np.exp(-self.V / 20.0)
        return 0.07 * np.exp(-(self.V + 65.0) / 20.0)

    def closingRateInactivationNa(self):
        # return 1 / (np.exp((30 - self.V) / 10) + 1)
        return 1.0 / (1.0 + np.exp(-(35.0 + self.V) / 10.0))






    def simulate(self):
        X = odeint(
        V.append(neuron.V)
        N.append(neuron.n)
        M.append(neuron.m)
        H.append(neuron.h)

        return V, N, M, H




if __name__ == "__main__":
    fun = lambda time: np.abs(np.sin(time)*3.1 + np.random.normal())*nA
    time = 190
    neuron = hh()
    electrode = electrode(const=3.5*nA/(mm**2))
    # electrode = electrode(fun=fun)
    electrode.connect(neuron)
    V, N, M, H = electrode.simulate(time)


    fig, ax = plt.subplots(2, 2, figsize=(10, 10))
    ax[0,0].plot(range(time), V)
    ax[0,0].set_title("V")

    ax[0,1].plot(range(time), N)
    ax[0,1].set_title("N")
    
    ax[1,0].plot(range(time), M)
    ax[1,0].set_title("M")

    ax[1,1].plot(range(time), H)
    ax[1,1].set_title("H")
    plt.show()

import scipy as sp
import pylab as plt
from scipy.integrate import odeint

class HodgkinHuxley():
    """Full Hodgkin-Huxley Model implemented in Python"""

    C_m  =   1.0
    """membrane capacitance, in uF/cm^2"""

    g_Na = 120.0
    """Sodium (Na) maximum conductances, in mS/cm^2"""

    g_K  =  36.0
    """Postassium (K) maximum conductances, in mS/cm^2"""

    g_L  =   0.3
    """Leak maximum conductances, in mS/cm^2"""

    E_Na =  50.0
    """Sodium (Na) Nernst reversal potentials, in mV"""

    E_K  = -77.0
    """Postassium (K) Nernst reversal potentials, in mV"""

    E_L  = -54.387
    """Leak Nernst reversal potentials, in mV"""

    t = sp.arange(0.0, 450.0, 0.01)
    """ The time to integrate over """

    def alpha_m(self, V):
        """Channel gating kinetics. Functions of membrane voltage"""
        return 0.1*(V+40.0)/(1.0 - sp.exp(-(V+40.0) / 10.0))

    def beta_m(self, V):
        """Channel gating kinetics. Functions of membrane voltage"""
        return 4.0*sp.exp(-(V+65.0) / 18.0)

    def alpha_h(self, V):
        """Channel gating kinetics. Functions of membrane voltage"""
        return 0.07*sp.exp(-(V+65.0) / 20.0)

    def beta_h(self, V):
        """Channel gating kinetics. Functions of membrane voltage"""
        return 1.0/(1.0 + sp.exp(-(V+35.0) / 10.0))

    def alpha_n(self, V):
        """Channel gating kinetics. Functions of membrane voltage"""
        return 0.01*(V+55.0)/(1.0 - sp.exp(-(V+55.0) / 10.0))

    def beta_n(self, V):
        """Channel gating kinetics. Functions of membrane voltage"""
        return 0.125*sp.exp(-(V+65) / 80.0)

    def I_Na(self, V, m, h):
        """
        Membrane current (in uA/cm^2)
        Sodium (Na = element name)

        |  :param V:
        |  :param m:
        |  :param h:
        |  :return:
        """
        return self.g_Na * m**3 * h * (V - self.E_Na)

    def I_K(self, V, n):
        """
        Membrane current (in uA/cm^2)
        Potassium (K = element name)

        |  :param V:
        |  :param h:
        |  :return:
        """
        return self.g_K  * n**4 * (V - self.E_K)
    #  Leak
    def I_L(self, V):
        """
        Membrane current (in uA/cm^2)
        Leak

        |  :param V:
        |  :param h:
        |  :return:
        """
        return self.g_L * (V - self.E_L)

    def I_inj(self, t):
        """
        External Current

        |  :param t: time
        |  :return: step up to 10 uA/cm^2 at t>100
        |           step down to 0 uA/cm^2 at t>200
        |           step up to 35 uA/cm^2 at t>300
        |           step down to 0 uA/cm^2 at t>400
        """
        return 10*(t>100) - 10*(t>200) + 35*(t>300) - 35*(t>400)

    @staticmethod
    def dALLdt(X, t, self):
        """
        Integrate

        |  :param X:
        |  :param t:
        |  :return: calculate membrane potential & activation variables
        """
        V, m, h, n = X

        dVdt = (self.I_inj(t) - self.I_Na(V, m, h) - self.I_K(V, n) - self.I_L(V)) / self.C_m
        dmdt = self.alpha_m(V)*(1.0-m) - self.beta_m(V)*m
        dhdt = self.alpha_h(V)*(1.0-h) - self.beta_h(V)*h
        dndt = self.alpha_n(V)*(1.0-n) - self.beta_n(V)*n
        return dVdt, dmdt, dhdt, dndt

    def Main(self):
        """
        Main demo for the Hodgkin Huxley neuron model
        """

        X = odeint(self.dALLdt, [-65, 0.05, 0.6, 0.32], self.t, args=(self,))
        V = X[:,0]
        m = X[:,1]
        h = X[:,2]
        n = X[:,3]
        ina = self.I_Na(V, m, h)
        ik = self.I_K(V, n)
        il = self.I_L(V)

        plt.figure()

        plt.subplot(4,1,1)
        plt.title('Hodgkin-Huxley Neuron')
        plt.plot(self.t, V, 'k')
        plt.ylabel('V (mV)')

        plt.subplot(4,1,2)
        plt.plot(self.t, ina, 'c', label='$I_{Na}$')
        plt.plot(self.t, ik, 'y', label='$I_{K}$')
        plt.plot(self.t, il, 'm', label='$I_{L}$')
        plt.ylabel('Current')
        plt.legend()

        plt.subplot(4,1,3)
        plt.plot(self.t, m, 'r', label='m')
        plt.plot(self.t, h, 'g', label='h')
        plt.plot(self.t, n, 'b', label='n')
        plt.ylabel('Gating Value')
        plt.legend()

        plt.subplot(4,1,4)
        i_inj_values = [self.I_inj(t) for t in self.t]
        plt.plot(self.t, i_inj_values, 'k')
        plt.xlabel('t (ms)')
        plt.ylabel('$I_{inj}$ ($\\mu{A}/cm^2$)')
        plt.ylim(-1, 40)

        plt.show()

if __name__ == '__main__':
    runner = HodgkinHuxley()
    runner.Main()
