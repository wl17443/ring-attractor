import numpy as np
from utils import compute_gain, plot_potentials
from lif_model import LIF


class RingAttractor:
    "A self-contained class for the ring attractor"

    def __init__(self,
                 n=128,
                 noise=2.0e-3,
                 # TODO: pick more stable fixed point weights
                 weights=(0.050, 0.088, 0.050, 0.15),
                 fixed_points_number=0, 
                 time=300,
                 plot=False):

        self.n = n
        self.noise = noise
        self.weights = weights
        self.fp_n = fixed_points_number
        self.time = time
        self.plot = plot

        self.neurons = [LIF(ID, noise_mean=0, noise_std=self.noise)
                        for ID in range(n)]

        # TODO: move weights, fp_n and noise to the simulate method
        self.fixed_points = self.get_fixed_points()

        self.connect_with_fixed_points()

    def simulate(self):

        mid_point = self.get_mid_point()

        potentials = [[] for _ in range(self.n)]
        for t in range(self.time):
            for neuron in self.neurons:

                self.input_source(mid_point=mid_point, n_of_spikes=5,
                                  weight=self.weights[0], begin_time=0, neuron=neuron, time=t)
                neuron.step()
                potentials[neuron.id].append(neuron.V)

        df, e = compute_gain(potentials, mid_point)

        if self.plot:
            plot_potentials(df, self.noise, self.weights,
                            self.fixed_points, e, self.time)

        return e

    def input_source(self, mid_point, n_of_spikes, weight, begin_time, neuron, time):
        sources = [i for i in range(mid_point - 2, mid_point + 3)]

        if time > begin_time:
            if neuron.id in sources:
                for _ in range(n_of_spikes):
                    neuron.exc_ps_td.append(
                        ((time - begin_time) * 1e-3, weight))

    def connect_with_fixed_points(self):
        for neur in self.neurons:
            if neur.id in self.fixed_points:
                for i in range(5, 12):
                    neur.synapses["inh"][self.neurons[(
                        neur.id + i) % self.n]] = self.weights[3]
                    neur.synapses["inh"][self.neurons[neur.id - i]
                                         ] = self.weights[3]
                for i in range(1, 5):
                    neur.synapses["exc"][self.neurons[(
                        neur.id + i) % self.n]] = self.weights[2]
                    neur.synapses["exc"][self.neurons[neur.id - i]
                                         ] = self.weights[2]

            else:
                for i in range(5, 12):
                    neur.synapses["inh"][self.neurons[(
                        neur.id + i) % self.n]] = self.weights[1]
                    neur.synapses["inh"][self.neurons[neur.id - i]
                                         ] = self.weights[1]
                for i in range(1, 5):
                    neur.synapses["exc"][self.neurons[(
                        neur.id + i) % self.n]] = self.weights[0]
                    neur.synapses["exc"][self.neurons[neur.id - i]
                                         ] = self.weights[0]

    def get_fixed_points(self):
        if self.fp_n == 0:
            return []

        index = np.arange(self.n)
        interval = self.n // self.fp_n

        distances = index % interval
        return np.where(distances < 3)[0]

    def get_mid_point(self):
        if self.fp_n <= 1:
            return self.n // 2


        free_points = set(np.arange(self.n)) - set(self.fixed_points)
        median = [*free_points][len(free_points) // 4]


        high = self.fixed_points[self.fixed_points > median][0]
        low = self.fixed_points[self.fixed_points < median][-1]
        mid_point = (high + low) // 2

        return mid_point


if __name__ == "__main__":

    np.random.seed(42)
    ring = RingAttractor(n=32, noise=3e-3, weights=(0.050, 0.088, 0.050, 0.250), fixed_points_number=2, time=100, plot=True)
    error = ring.simulate()
