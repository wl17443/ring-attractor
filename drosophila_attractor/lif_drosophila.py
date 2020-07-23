# Leaky integrate and fire model

ms = 10e-3
mV = 10e-3
uf = 10e-6
nA = 10e-9
MOhm = 10e6


class lif:
    El   = -52.0 * mV      # Leaky reversal potential
    Cm   = 0.002 * uF      # Membrane capacitance
    Rm   = 10.0 * MOhm     # Membrane resistance
    Vthr = -54.0 * mV      # Threshold potential
    Vmax = 20 * mV         # Peak action potential, purely cosmetic
    Vmin = -72.0 * mV      # Spike undershoot voltage, not exactly reset potential
    tap  = 2.0 * ms        # Lenght of action potential
    ts   = 1               # Time from last spike

    Ipsc = 5.0 * nA        # Amplitude of post-synaptic-current
    tpsc = 2.0 * ms        # Half-life of PSC decay
    Iex  = 0.0 * nA        # External current, 0 unless neuron is E-PG
    Is   = 0.0 * nA        # Total synaptic current

    def __init__(self, ID):
        self.id = ID
        self.Is = 0.0      # Synpatic Current
        self.synapses = {} # neuron: weight

        self.V = self.El   # Membrane potential, set at equilibrium

    def step(self):
        if ts < tap:
            self._spikingMechanism


        self._updateSynapticCurrent()
        self._updatePotential()
        self._checkSpike()

    def _updatePotential(self):
        self.V += ((self.El - self.V)/self.Rm + self.Iex + self.Is) / self.Cm * ms


    def _checkSpike(self):
        self.ts = 0
        if self.V >= self.Pthr:
            self.ts = 0.0

    def _spikingMechanism(self):
        if self.ts < self.tap

    def _updateSynapticCurrent(self):
        self.Is = 0.0
        self.Is += self.Ip

        for neuron, weight in self.synapses.items():
            if neuron.V == 0.0:
                self.Is += weight
