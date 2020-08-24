from datetime import datetime
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


# TODO: explore parameters of this function
def calculate_weights(weights, fp_n=16, total_neurons=128):
    if fp_n >= 1:
        new_weights = [0, 0, 0, 0]
        new_weights[0] = 0.9 * weights[0]
        new_weights[1] = 0.9 * weights[1]
        new_weights[2] = (0.1 * total_neurons/fp_n + 1) * weights[0]
        new_weights[3] = (0.1 * total_neurons/fp_n + 1) * weights[1]
    else:
        new_weights = weights
    return new_weights


def compute_stats(potentials, n, time, starting_point):
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
    error = np.abs(mean_of_medians - starting_point)

    return df, error


def plot_potentials(df, noise, weights, fixed_points, error, time):
    _, ax = plt.subplots(figsize=(10, 10))
    sns.heatmap(df, vmin=-0.08, vmax=0.0, cmap="viridis", xticklabels=int(time/10),
                yticklabels=5, cbar_kws={'label': "Membrane Potential (V)"}, ax=ax)
    plt.xlabel("Time (ms)")
    plt.ylabel("# of neuron")
    plt.subplots_adjust(left=0.07, bottom=0.07, right=0.97, top=0.89)

    labels = [item.get_text() for item in ax.get_yticklabels()]

    for i, l in enumerate(labels):
        if int(l) in fixed_points:
            labels[i] = labels[i] + '\nFP'

    ax.set_yticklabels(labels)

    ax.set_title("Number of fixed points: {}\nNoise: {:.2E}\nWeights: {}\nError: {}".format(
        len(fixed_points) // 3, noise, weights, round(error, 2)))

    plt.savefig(
        f"images/{datetime.now().strftime('%d-%m-%Y, %H:%M:%S')}.png")
    plt.show()


def plot_errors(csv_name):
    _, ax = plt.subplots(figsize=(10, 10))
    df = pd.read_csv(csv_name, index_col=0)
    sns.barplot(df.index, df.errors, ax=ax, palette=sns.cubehelix_palette(8))

    ax.set_ylabel("Absolute Error")
    ax.set_xlabel("# of Fixed Points")
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    plt.savefig("errors.png")
    plt.show()
