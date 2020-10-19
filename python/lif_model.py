from numpy import exp
from numpy.random import normal

mV = 1e-3
nF = 1e-9
ms = 1e-3


class LIF:
    "Leaky integrate and fire model"

    Vthr = -48.0 * mV  # Threshold potential
    Cm = 1.0 * nF
    Einh = -70.0 * mV
    Eexc = 0.0 * mV
    Em = -70.0 * mV
    tau_ref = 2.0 * ms
    tau_syn_inh = 5.0 * ms
    tau_syn_exc = 5.0 * ms
    tau_m = 5.0 * ms  # Membrane time constant
    El = -70.0 * mV  # Leaky reversal potential
    Vr = -80.0 * mV  # Reset potential

    def __init__(self, ID, angle, dt=1, noise_mean=0, noise_std=1):
        self.id = ID
        self.Iext = 0.0
        self.V = self.Vr  # Membrane potential, set at reset
        self.dt = dt * ms
        self.time_from_spike = 200.0 * ms
        self.kexc = 1 / (self.tau_syn_exc * exp(-1))
        self.kinh = 1 / (self.tau_syn_inh * exp(-1))

        # outgoing synapses, {neuron: weight}
        self.synapses = {"inh": {}, "exc": {}}
        # exc and inh pre-synaptic time delays from last spike, [(time_delay, weight), (...)]
        self.inh_ps_td = []
        self.exc_ps_td = []

        self.noise_mean = noise_mean
        self.noise_std = noise_std

        self.angle = angle

    def step(self):

        # If spiked, hyperpolarize
        if self.V == 0.0:
            self.V = self.Vr

        # If above threshold, depolarize
        elif self.V >= self.Vthr:
            self.V = 0.0
            self.time_from_spike = 0

        # elif self.time_from_spike > self.tau_ref:
        #     pass

        # Else, update Current with Euler
        else:
            self.V += self.dV() * self.dt + self.noise()

        # Send time delays to connected neurons
        if self.time_from_spike > self.tau_ref:
            for neuron, weight in self.synapses["inh"].items():
                neuron.inh_ps_td.append((self.time_from_spike, weight))
            for neuron, weight in self.synapses["exc"].items():
                neuron.exc_ps_td.append((self.time_from_spike, weight))

        self.time_from_spike += self.dt

        # Reset time delays
        self.inh_ps_td.clear()
        self.exc_ps_td.clear()

    def dV(self):
        return (-self.Il() - self.Is_inh() - self.Is_exc()) / self.Cm

    def Il(self):
        return self.Cm / self.tau_m * (self.V - self.El)

    def Is_inh(self):
        I = 0.0
        for td, w in self.inh_ps_td:
            I += (self.Ginh(td) * (self.V - self.Einh)) * w * 1e-6

        return I

    def Is_exc(self):
        I = 0.0
        for td, w in self.exc_ps_td:
            I += (self.Gexc(td) * (self.V - self.Eexc)) * w * 1e-6

        return I

    def Gexc(self, t):
        return self.kexc * t * exp(-t/self.tau_syn_exc)

    def Ginh(self, t):
        return self.kinh * t * exp(-t/self.tau_syn_inh)

    def noise(self):
        return normal(self.noise_mean, self.noise_std)
