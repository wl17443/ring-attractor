# Leaky integrate and fire model
from scipy.stats import norm
from numpy import sin, pi, arange
from units import *


class lif:
    El = -52.0 * mV        # Leaky reversal potential
    Cm = 0.002 * uF        # Membrane capacitance
    Rm = 10.0 * MOhm       # Membrane resistance
    Vthr = -54.0 * mV      # Threshold potential
    Vmax = 20 * mV         # Peak action potential, purely cosmetic
    Vmin = -72.0 * mV      # Spike undershoot voltage, not exactly reset potential
    tap = 2.0 * ms         # Lenght of action potential
    ts = 1                 # Time from last spike

    Ipsc = 5.0 * nA        # Amplitude of post-synaptic-current
    tpsc = 2.0 * ms        # Half-life of PSC decay
    Iex = 0.0 * nA         # External current, 0 unless neuron is E-PG
    Is = 0.0 * nA          # Total incoming synaptic current
    Iout = 0.0 * nA        # Output current

    def __init__(self, ID):
        self.id = ID
        self.dt = 0.1 * ms  # Timestep
        self.Is = 0.0       # Synpatic Current
        self.synapses = {}  # neuron: weight

        self.V = self.El    # Membrane potential, set at equilibrium

    def step(self):
        if self.ts < self.tap:
            self._spikingMechanism()

        self._computePSC()
        self._injectPSC()

        self._updatePotential()

        self.Is = 0.0 * nA  # Reset input currents

        self.ts += self.dt
        if self.V >= self.Vthr:
            self.ts = 0.0

    def _updatePotential(self):
        self.V += ((self.El - self.V)/self.Rm +
                   self.Iex + self.Is) / self.Cm * self.dt

    def _computePSC(self):
        # TODO move the stuff inside here somewhere else, it need to be initialized only one time
        PSCtrace = self.tap * 7 + 2 * ms

        def Irise(t):
            return sin(t * pi / 2 - pi / 2)
        risetime = arange(0, 2 * ms, self.dt)
        riseMin = min([Irise(t) for t in risetime])
        riseMax = max([Irise(t) for t in risetime])

        def Ifall(t):
            return 2 ** (-(t - 2)/self.tpsc)
        falltime = arange(2 * ms, PSCtrace, self.dt)
        fallMin = min([Ifall(t) for t in falltime])
        fallMax = max([Ifall(t) for t in falltime])

        if self.ts > PSCtrace:
            self.Iout = 0.0 * nA
        elif self.ts < 2 * ms:
            self.Iout = self.Ipsc * \
                (Irise(self.ts) - riseMin)/(riseMax - riseMin)
        else:
            self.Iout = self.Ipsc * \
                (Ifall(self.ts) - fallMin)/(fallMax - fallMin)

    def _spikingMechanism(self):
        # TODO move the stuff inside here somewhere else, it need to be initialized only one time

        def apRise(t):
            return norm.pdf(-1 + t / (self.tap / 2))
        risetime = arange(0, self.tap/2, self.dt)
        riseMin = min([apRise(t) for t in risetime])
        riseMax = max([apRise(t) for t in risetime])

        def apFall(t):
            return sin((t - self.tap/2) * pi/self.tap + pi/2)
        falltime = arange(self.tap/2, self.tap, self.dt)
        fallMin = min([apFall(t) for t in falltime])
        fallMax = max([apFall(t) for t in falltime])

        if self.ts < self.tap/2:
            self.V = self.Vthr + (self.Vmax - self.Vthr) * \
                (apRise(self.ts) - riseMin)/(riseMax - riseMin)
        else:
            self.V = self.Vmin + (self.Vmax - self.Vmin) * \
                (apFall(self.ts) - fallMin)/(fallMax - fallMin)

    def _injectPSC(self):
        for neuron, weight in self.synapses.items():
            neuron.Is += weight * self.Iout
