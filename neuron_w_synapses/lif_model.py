# Leaky integrate and fire model

ms = 0.001
mV = 0.001


class lif:
    tau = 20.0 * ms
    Rl = -70.0 * mV
    Pr = -80.0 * mV

    Ip = 0.0  # Input from poisson
    Pthr = -54.0 * mV

    def __init__(self, ID):
        self.id = ID
        self.Is = 0.0
        self.synapses = {}  # neuron: weight

        self.V = self.Pr

    def step(self):
        self._hyperpolarize()

        self._updateIs()
        self._updateV()
        self._depolarize()

    def _updateV(self):
        self.V += (self.Rl - self.V + self.Is * self.tau) / self.tau * ms

    def _hyperpolarize(self):
        if self.V == 0.0:
            self.V = self.Pr

    def _depolarize(self):
        if self.V >= self.Pthr:
            self.V = 0.0

    def _updateIs(self):
        self.Is = 0.0
        self.Is += self.Ip

        for neuron, weight in self.synapses.items():
            if neuron.V == 0.0:
                self.Is += weight
