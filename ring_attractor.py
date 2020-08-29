import numpy as np
from utils import compute_stats, plot_potentials
from lif_model import LIF


class RingAttractor:
    "A self-contained class for the ring attractor"

    def __init__(self,
                 n=128,
                 noise=2.5e-3,
                 weights=(0.050, 0.088, 0.050, 0.15),
                 fixed_points_number=0,
                 random_seed=None):

        self.n = n
        self.noise = noise
        self.weights = weights
        self.fp_n = fixed_points_number
        self.random_seed = random_seed

        self.neurons = [LIF(ID, noise_mean=0, noise_std=self.noise)
                        for ID in range(n)]
        self.fp_width = 3
        self.fixed_points = self.get_fixed_points()

        self.connect_with_fixed_points()

        if random_seed:
            np.random.seed(self.random_seed)

    def simulate(self, time=300, plot=False):

        mid_point = self.get_mid_point()

        potentials = [[] for _ in range(self.n)]
        for t in range(time):
            for neuron in self.neurons:

                self.input_source(mid_point=mid_point, n_of_spikes=5,
                                  weight=self.weights[0], begin_time=0, neuron=neuron, time=t)
                neuron.step()
                potentials[neuron.id].append(neuron.V)

        df, e = compute_stats(potentials, self.n, time, mid_point)

        if plot:
            plot_potentials(df, self.noise, self.weights,
                            self.fixed_points, e, time, self.fp_width, self.random_seed)

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
        
        return np.where(distances < self.fp_width)[0]

    def get_mid_point(self):
        standard = 45
        if len(self.fixed_points) < 4:
            return standard

        idx = np.where(self.fixed_points > standard)[0][0]
        mid_point = round(
            np.mean([self.fixed_points[idx], self.fixed_points[idx-1]]))

        return int(mid_point)


if __name__ == "__main__":

    # ext, inh, fp ext, inh
    ring = RingAttractor(noise=2.0e-3, fixed_points_number=4, random_seed=None)
    error = ring.simulate(time=100, plot=True)
