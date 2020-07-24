from numpy import exp

mV = 1e-3
nF = 1e-9
ms = 1e-3


class LIF:
    "Leaky integrate and fire model"

    Vthr = -48.0 * mV  # Threshold potential
    Cm = 1 * nF
    Einh = -70 * mV
    Eexc = 0.0 * mV
    Em = -70 * mV
    tau_ref = 2 * ms
    tau_syn_inh = 5.0 * ms
    tau_syn_exc = 5.0 * ms
    tau_m = 20.0 * ms  # Membrane time constant
    El = -70.0 * mV  # Leaky reversal potential
    Vr = -80.0 * mV  # Reset potential

    def __init__(self, ID, dt=1):
        self.id = ID
        self.Iext = 0.0
        self.V = self.Vr  # Membrane potential, set at reset
        self.dt = dt * ms
        self.time_from_spike = 1
        self.kexc = 1 / (self.tau_syn_exc * exp(-1))
        self.kinh = 1 / (self.tau_syn_inh * exp(-1))

        self.synapses = {}  # outgoing synapses, {neuron: weight}
        # exc and inh pre-synaptic time delays from last spike, [(time_delay, weight), (...)]
        self.inh_ps_td = []
        self.exc_ps_td = []

    def step(self):

        # If spiked, hyperpolarize
        if self.V == 0.0:
            self.V = self.Vr

        # If above threshold, depolarize
        elif self.V >= self.Vthr:
            self.V = 0.0
            self.time_from_spike = 0

        # Else, update Current with Euler
        else:
            self.V += self.dV() * self.dt

        # Send time delays to connected neurons
        for neuron, weight in self.synapses.items():
            if weight < 0:
                neuron.inh_ps_td.append((self.time_from_spike, weight))
            if weight > 0:
                neuron.exc_ps_td.append((self.time_from_spike, weight))

        self.time_from_spike += self.dt

        # Reset time delays
        self.inh_ps_td.clear()
        self.exc_ps_td.clear()

    def dV(self):
        return (-self.Il() - self.Is_inh() - self.Is_exc() +
                self.Iext) / self.Cm

    def Il(self):
        return self.Cm / self.tau_m * (self.V - self.El)

    def Is_inh(self):
        I = 0
        if self.time_from_spike > self.tau_ref:
            for td, w in self.inh_ps_td:
                Is = self.Ginh(td) * (self.V - self.Einh)
                Is *= w
                I += Is

        return I

    def Is_exc(self):
        I = 0
        if self.time_from_spike > self.tau_ref:
            for td, w in self.exc_ps_td:
                Is = self.Gexc(td) * (self.V - self.Eexc)
                Is *= w
                I += Is

        return I

    def Gexc(self, t):
        return self.kexc * t * exp(-t/self.tau_syn_exc)

    def Ginh(self, t):
        return self.kinh * t * exp(-t/self.tau_syn_inh)
