# Leaky integrate and fire model
from numpy import exp

mV = 1e-3
nF = 1e-9
ms = 1e-3


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
        self.ts = 2.0
        self.kexc = 1 / (self.tau_syn_exc * exp(-1))
        self.kinh = 1 / (self.tau_syn_inh * exp(-1))

        self.synapses = {}  # neuron: weight
        self.abc = {-1: [], 1: []}

    def step(self):

        if self.V == 0.0:
            self.V = self.Vr
            return

        self._updateCurrents()
        self._updatePotential()
        self._injectCurrents()
        self._check_depolarize()

        self.ts += self.dt

    def _updatePotential(self):
        if self.ts > self.tau_ref:
            self.V += (-self.Il - self.Is_inh - self.Is_exc +
                       self.Iext) / self.Cm * self.dt


    def _check_depolarize(self):
        if self.V >= self.Vthr:
            self.V = 0.0
            self.ts = 0

    def Gexc(self, t):
        return self.kexc * t * exp(-t/self.tau_syn_exc)

    def Ginh(self, t):
        return self.kinh * t * exp(-t/self.tau_syn_inh)

    def _updateCurrents(self):
        self.Il = self.Cm/self.tau_m * (self.V - self.El)

        self.Is_inh = 0 
        self.Is_exc = 0
        if self.ts > self.tau_ref:
            for w, times in self.abc.items():
                if w == -1 :
                    for ts in times:
                        self.Is_inh -= self.Ginh(ts) * (self.V - self.Einh)

                if w == 1:
                    for ts in times:
                        self.Is_exc += self.Gexc(ts) * (self.V - self.Eexc)

        self.abc = {-1: [], 1: []}


    def _injectCurrents(self):
        for neuron, weight in self.synapses.items():
            if weight != 0:
                neuron.abc[int(weight)].append(self.ts)

