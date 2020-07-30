import numpy as np
import pandas as pd
from connect import connect_with_fixed_points
from LIF_Model import LIF
from Plot import plot_potentials

def simulate(weights, fp_n, noise, plot=False, starting_point=44):
    time = 1000
    n = 128
    dt = 1
    starting_points = [i for i in range(
        starting_point - 2, starting_point + 3)]
    spike_source = [c for c in starting_points]

    neurons = [LIF(ID, dt=dt, noise_mean=0, noise_std=noise)
               for ID in range(n)]

    fixed_points = connect_with_fixed_points(neurons, n, weights, fp_n=fp_n)

    def input_source(indexes, n_of_spikes, begin_time, neuron, time):
        if time > begin_time:
            if neuron.id in indexes:
                for _ in range(n_of_spikes):
                    neuron.exc_ps_td.append(
                        ((t - begin_time) * 1e-3, weights[0]))

    potentials = [[] for _ in range(n)]
    for t in range(time):
        for neuron in neurons:

            input_source(spike_source, 5, 0, neuron, t)

            neuron.step()

            potentials[neuron.id].append(neuron.V)

    # Stats

    df = pd.DataFrame(potentials)
    spikes = df == 0.0
    spikes = spikes.astype(int)
    spikes = spikes.loc[:, time-100:]
    for i in range(n):
        spikes.loc[i] = spikes.loc[i] * i

    medians = []
    for i in range(time - 100, time):
        medians.append(spikes[i].loc[spikes[i] != 0.0].median())

    medians = pd.Series(medians).dropna()
    mean_of_medians = np.mean(medians)
    error = np.abs(mean_of_medians - np.median(starting_points))
    var_of_medians = np.var(medians)

    if plot:
        plot_potentials(df, noise, weights, fixed_points, error, var_of_medians, time)

    return error, var_of_medians


if __name__ == "__main__":

    # ext, inh, fp ext, inh
    _weights = [0.050, 0.088, 0.050, 0.095]

    e, v = simulate(_weights, fp_n=8, noise=3.5e-3,
                    starting_point=40, plot=True)
