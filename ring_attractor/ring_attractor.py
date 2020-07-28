import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from datetime import datetime
from tqdm import tqdm
from connect import connect_with_fixed_points
from lif_model import LIF


def simulate(weights, fp_n, noise, plot=False): 
    time = 300
    n = 128
    dt = 1
    starting_points = [46, 47, 48, 49, 50]
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

            input_source(spike_source, 5, 0, neuron, t)

            neuron.step()

            potentials[neuron.id].append(neuron.V)

# Plots

    df = pd.DataFrame(potentials)
    spikes = df == 0.0
    spikes = spikes.astype(int)
    for i in range(n):
        spikes.loc[i] = spikes.loc[i] * i

    medians = []
    for i in range(time):
        medians.append(spikes[i].loc[spikes[i] != 0.0].median())


    medians = pd.Series(medians).dropna()
    mean_of_medians = np.mean(medians)
    var_of_medians = np.var(medians)

    
    if plot:
        fig, ax = plt.subplots(figsize=(10,10))
        sns.heatmap(df, vmin=-0.08, vmax=0.0, cmap="viridis", xticklabels=int(time/10), yticklabels=5, cbar_kws={'label':"Membrane Potential (V)"}, ax=ax)
        plt.xlabel("Time (ms)")
        plt.ylabel("# of neuron")
        plt.subplots_adjust(left=0.07, bottom=0.07, right=0.97, top=0.95)

        labels = [item.get_text() for item in ax.get_yticklabels()]

        for i, l in enumerate(labels):
            if int(l) in fixed_points:
                labels[i] = labels[i] + '\nFP'

        ax.set_yticklabels(labels)

        ax.set_title("Mean of medians: {}\nVar of median: {}".format(round(mean_of_medians, 2), round(var_of_medians, 2)))
            

        plt.savefig(f"images/{datetime.now().strftime('%d-%m-%Y, %H:%M:%S')}.png")
        plt.show()

    return np.abs(mean_of_medians - np.median(starting_points)), var_of_medians


if __name__ == "__main__":

    weights = [0.025, 0.05, 0.090, 0.3]  # ext, inh, fp ext, inh
    error, var = simulate(weights, fp_n=0, noise=2e-3)

    fixed_points = [2, 4, 8, 16, 32, 64, 128]
    noises = np.linspace(2e-3, 2.3e-3, num=20)

    records = pd.DataFrame(index=fixed_points, columns = noises)
    var_records = pd.DataFrame(index=fixed_points, columns = noises)

    for n in tqdm(noises):
        for i in fixed_points:
            errors = []
            variances = []

            for _ in range(10):
                e, v = simulate(weights, fp_n=i, noise=n)
                errors.append(e)
                variances.append(v)

            records.loc[i, n] = np.mean(errors)
            var_records.loc[i, n] = np.mean(variances)


    records.to_csv("error_by_noise.csv", index=False)
    var_records.to_csv("var_by_noise.csv", index=False)



