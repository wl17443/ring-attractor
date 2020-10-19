import numpy as np
from numba import njit

nF = 1e-9
mV = 1e-3
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
        self.kexc = 1 / (self.tau_syn_exc * np.exp(-1))
        self.kinh = 1 / (self.tau_syn_inh * np.exp(-1))
        self.Iext = 0
        self.angle = angle

        # outgoing synapses, {neuron: weight}
        self.synapses = {"inh": {}, "exc": {}}
        # exc and inh pre-synaptic time delays from last spike, [(time_delay, weight), (...)]
        self.inh_ps_td = [(0, 0)]
        self.exc_ps_td = [(0, 0)]

        self.noise_mean = noise_mean
        self.noise_std = noise_std

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
            self.V += _dv(self.V, self.Cm, self.El, self.Eexc, self.Einh, self.tau_m, self.tau_syn_inh, self.tau_syn_exc, self.dt,
                          np.random.normal(self.noise_mean, self.noise_std), np.array(self.inh_ps_td), np.array(self.exc_ps_td), self.kexc, self.kinh, self.Iext)

        # Send time delays to connected neurons
        if self.time_from_spike > self.tau_ref:
            for neuron, weight in self.synapses["inh"].items():
                neuron.inh_ps_td.append((self.time_from_spike, weight))
            for neuron, weight in self.synapses["exc"].items():
                neuron.exc_ps_td.append((self.time_from_spike, weight))

        self.time_from_spike += self.dt

        # Reset time delays
        self.inh_ps_td = [(0, 0)]
        self.exc_ps_td = [(0, 0)]


@njit(cache=True)
def _dv(v, Cm, El, Eexc, Einh, tau, tau_syn_inh, tau_syn_exc, dt, noise, inh_ps_td, exc_ps_td, kexc, kinh, Iext):

    I_inh = 0.0
    I_exc = 0.0

    for td, w in inh_ps_td:
        I_inh += (kinh * td * np.exp(-td/tau_syn_inh)) * w * 1e-6 * (v - Einh)

    for td, w in exc_ps_td:
        I_exc += (kexc * td * np.exp(-td/tau_syn_exc)) * w * 1e-6 * (v - Eexc)

    dv = ((-Cm / tau * (v - El) - I_inh - I_exc + Iext) / Cm) * \
        dt + noise

    return dv


if __name__ == "__main__":

    from time import time
    import matplotlib.pyplot as plt

    def sim():
        start = time()
        stim_time = 20000
        total_time = 20000

        neuron = LIF(1, 0, dt=0.25, noise_std=0)
        params = {"V": [], "Iext": [], "SpikeTimes": []}
        neuron.Iext = 70 * 1e-9

        assert stim_time <= total_time

        for t in range(total_time):
            if t == stim_time:
                neuron.Iext = 0.0
            neuron.step()

            params["V"].append(neuron.V)
            params["Iext"].append(neuron.Iext)

            if neuron.V == 0:
                params["SpikeTimes"].append(t)

        end = time()
        return end-start

        fig, ax = plt.subplots(5, figsize=(7, 10))
        plt.subplots_adjust(left=0.08, bottom=0.05,
                            right=0.97, top=0.95, hspace=0.35)

        ax[0].plot(params["V"])
        ax[0].set_title('Potential')

        ax[1].plot(params["Iext"], color='r')
        ax[1].set_title('Step external current')
        plt.show()

    print("[numba] Computing voltage for 1 neuron stimulated for 20 second...")
    print("Time elapsed: ", sim())

