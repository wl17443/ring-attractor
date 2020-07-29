import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from datetime import datetime
from tqdm import tqdm
from connect import connect_with_fixed_points
from lif_model import LIF


def simulate(weights, fp_n, noise, plot=False, starting_point=44): 
    time = 1000
    n = 128
    dt = 1
    starting_points = [i for i in range(starting_point - 2, starting_point + 3)]
    spike_source = [c for c in starting_points]

    neurons = [LIF(ID, dt=dt, noise_mean=0, noise_std=noise) for ID in range(n)]


    fixed_points = connect_with_fixed_points(neurons, n, weights, fp_n=fp_n)

    def input_source(indexes, n_of_spikes, begin_time, neuron, time):
            if time > begin_time:
                if neuron.id in indexes:
                    for _ in range(n_of_spikes):
                        neuron.exc_ps_td.append(((t - begin_time) *  1e-3, weights[0]))


    potentials = [[] for _ in range(n)]
    for t in range(time):
        for neuron in neurons:

            input_source(spike_source, 150, 0, neuron, t)

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
        # Plots
        fig, ax = plt.subplots(figsize=(10,10))
        sns.heatmap(df, vmin=-0.08, vmax=0.0, cmap="viridis", xticklabels=int(time/10), yticklabels=5, cbar_kws={'label':"Membrane Potential (V)"}, ax=ax)
        plt.xlabel("Time (ms)")
        plt.ylabel("# of neuron")
        plt.subplots_adjust(left=0.07, bottom=0.07, right=0.97, top=0.90)

        labels = [item.get_text() for item in ax.get_yticklabels()]

        for i, l in enumerate(labels):
            if int(l) in fixed_points:
                labels[i] = labels[i] + '\nFP'

        ax.set_yticklabels(labels)

        ax.set_title("Noise: {:.2E}\nWeights: {}\nError: {}\nVar of median: {}".format(noise, weights, round(error, 2), round(var_of_medians, 2)))
            

        plt.savefig(f"images/{datetime.now().strftime('%d-%m-%Y, %H:%M:%S')}.png")
        plt.show()

    return error, var_of_medians


if __name__ == "__main__":

    weights = [0.035, 0.088, 0.050, 0.095]  # ext, inh, fp ext, inh RIGHT WEIGHTS FOR 32 FP
    # weights = [0.050, 0.088, 0.025, 0.08]  

    e, v = simulate(weights, fp_n=8, noise=3.0e-3, starting_point=40, plot=True)


