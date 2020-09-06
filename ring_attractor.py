from datetime import datetime
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from utils import circular_mean
from lif_model import LIF
import warnings


class RingAttractor:
    "A self-contained class for the ring attractor"

    def __init__(self,
                 n=128,
                 noise=2.0e-3,
                 weights=(0.050, 0.100, 0.050, 0.250),
                 fixed_points_number=0,
                 time=1000,
                 plot=False,
                 random_seed=None):

        self.n = n
        self.noise = noise
        self.weights = weights
        self.fp_n = fixed_points_number
        self.time = time
        self.plot = plot
        self.random_seed = random_seed
        self.neurons = [LIF(ID=i, angle=360.0/n*i, noise_mean=0, noise_std=self.noise,) for i in range(n)]
        self.fp_width = 3
        self.fixed_points = self.get_fixed_points()
        self.mid_point = self.get_mid_point()

        self.connect_with_fixed_points()
        self.flushed = 0

        if random_seed:
            np.random.seed(self.random_seed)

    def simulate(self):
        if self.flushed == 1:
            warnings.warn("Simulation has not been flushed!")

        potentials = [[] for _ in range(self.n)]
        for t in range(self.time):
            for neuron in self.neurons:

                self.input_source(n_of_spikes=5, begin=0,
                                  neuron=neuron, time=t)
                neuron.step()
                potentials[neuron.id].append(neuron.V)

        df, err = self.compute_loss(potentials)

        if self.plot:
            self.plot_potentials(df, err)

        return err

    def compute_loss(self, potentials):
        df = pd.DataFrame(potentials)
        df.index = [self.neurons[i].angle for i in df.index]
        spikes = df == 0.0

        spikes = spikes.iloc[:, -30:]
        spikes = spikes.astype(int)
        spikes = spikes.apply(lambda x: x * x.index)
        spikes = spikes.replace(0, np.nan)

        means = spikes.apply(circular_mean, axis=0)
        total_mean = circular_mean(means)
        err = np.abs(self.neurons[self.mid_point].angle - total_mean)

        return df, err

    def input_source(self, n_of_spikes, begin, neuron, time):
        sources = [i for i in range(self.mid_point - 2, self.mid_point + 3)]

        if time > begin:
            if neuron.id in sources:
                for _ in range(n_of_spikes):
                    neuron.exc_ps_td.append(
                        ((time - begin) * 1e-3, self.weights[0]))
                    
    def flush(self,neurons=True,fixed_points=True,connections=True):
        # Reset the model so simulations can be re-run without carrying 
        # activity over
        if neurons:
            self.neurons = [LIF(ID, noise_mean=0, noise_std=self.noise)
                            for ID in range(self.n)]
        if fixed_points:
            self.fixed_points=self.get_fixed_points()
        if connections:
            self.connect_with_fixed_points()
        self.flushed = 0
        

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
        if self.fp_n <= 1:
            return self.n // 2

        free_points = set(np.arange(self.n)) - set(self.fixed_points)
        median = [*free_points][len(free_points) // 4]

        high = self.fixed_points[self.fixed_points > median][0]
        low = self.fixed_points[self.fixed_points < median][-1]
        mid_point = (high + low) // 2

        return mid_point

    def plot_potentials(self, df, err):
        _, ax = plt.subplots(figsize=(10, 10))
        sns.heatmap(df, vmin=-0.08, vmax=0.0, cmap="viridis", xticklabels=int(self.time/10),
                    yticklabels=10, cbar_kws={'label': "Membrane Potential (V)"}, ax=ax)


        for target in np.arange(0,len(self.fixed_points),self.fp_width):
            cur_fixed_point = np.mean(self.fixed_points[target:(target+self.fp_width)])
            plt.plot([0,self.time],[cur_fixed_point,cur_fixed_point],color='k')

        plt.xlabel("Time (ms)")
        plt.ylabel("Orientation of neuron")
        plt.subplots_adjust(left=0.07, bottom=0.07, right=0.97, top=0.88)

        ax.set_title("Number of fixed points: {}\nNoise: {:.3e}\nWeights: {}\nError: {:.3f}\nRandom seed: {}".format(
            self.fp_n, self.noise, self.weights, err, self.random_seed))

        plt.savefig(
            f"images/{datetime.now().strftime('%d-%m-%Y, %H:%M:%S')}.png")
        plt.show()



if __name__ == "__main__":

    # np.random.seed(42)
    ring = RingAttractor(n=256, noise=1.5e-3, weights=(0.050, 0.100, 0.050, 0.250), fixed_points_number=32, time=100, plot=True, random_seed=None)
    error = ring.simulate()
