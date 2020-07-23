# Leaky integrate and fire model

ms = 0.001
mV = 0.001


class lif:
    tau = 20.0 * ms # Membrane time constant
    El = -70.0 * mV # Leaky reversal potential
    Vr = -80.0 * mV # Reset potential

    Ip = 0.0  # Input from poisson
    Vthr = -54.0 * mV # Threshold potential

    def __init__(self, ID):
        self.id = ID
        self.Is = 0.0 # Synpatic Current
        self.synapses = {}  # neuron: weight

        # TODO should it be random?
        self.V = self.Vr # Membrane potential, set at reset

    def step(self):
        self._check_hyperpolarize()

        self._updateSynapticCurrent()
        self._updatePotential()
        self._check_depolarize()

    def _updatePotential(self):
        self.V += (self.El - self.V + self.Is * self.tau) / self.tau * ms

    def _check_hyperpolarize(self):
        if self.V == 0.0:
            self.V = self.Vr

    def _check_depolarize(self):
        if self.V >= self.Vthr:
            self.V = 0.0

    def _updateSynapticCurrent(self):
        self.Is = 0.0
        self.Is += self.Ip

        for neuron, weight in self.synapses.items():
            if neuron.V == 0.0:
                self.Is += weight
