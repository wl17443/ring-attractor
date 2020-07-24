# Leaky integrate and fire model
from numpy import exp

mV = 10e-3
nF = 10e-9
ms = 10e-3


class lif:
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

    def __init__(self, ID):
        self.id = ID
        self.Is_exc = 0.0  # Synpatic Current
        self.Is_inh = 0.0  # Synpatic Current
        self.Il = 0.0  # Leakeage current
        self.Iext = 0.0
        self.V = self.Vr  # Membrane potential, set at reset
        self.dt = 1 * ms
        self.ts = 1
        self.kexc = 1 / (self.tau_syn_exc * exp(-1))
        self.kinh = 1 / (self.tau_syn_inh * exp(-1))
        self.ts = 0

        self.synapses = {}  # neuron: weight

    def step(self):
        self._check_hyperpolarize()

        self._updateCurrents()
        self._updatePotential()
        self._check_depolarize()

        self.Iext = 0.0
        self.Is_exc = 0.0
        self.Is_inh = 0.0
        self.ts += self.dt

    def _updatePotential(self):
        self.V += (-self.Il - self.Is_inh - self.Is_exc +
                   self.Iext) / self.Cm * self.dt

    def _check_hyperpolarize(self):
        if self.V == 0.0:
            self.V = self.Vr

    def _check_depolarize(self):
        if self.V >= self.Vthr:
            self.V = 0.0
            # self.ts = 0

    def Gexc(self, ts):
        return self.kexc * ts * exp(-ts/self.tau_syn_exc)

    def Ginh(self, ts):
        return self.kinh * ts * exp(-ts/self.tau_syn_inh)

    def _updateCurrents(self):
        self.Il = self.Cm/self.tau_m * (self.V - self.El)
        self.Is_inh = self.Ginh(self.ts) * (self.V - self.Einh)
        self.Is_exc = self.Gexc(self.ts) * (self.V - self.Eexc)

    def _injectCurrent(self):
        for neuron, weight in self.synapses.items():
            if self.ts > self.tau_ref:
                neuron.Is_inh = weight * (self.Ginh(self.ts) * (self.V - self.Einh))
                neuron.Is_exc = weight * (self.Gexc(self.ts) * (self.V - self.Eexc))
