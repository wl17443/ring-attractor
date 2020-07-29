# Plots
import seaborn as sns
import matplotlib.pyplot as plt
from datetime import datetime


def plot_potentials(df, noise, weights, fixed_points, error, var_of_medians, time):
    fig, ax = plt.subplots(figsize=(10, 10))
    sns.heatmap(df, vmin=-0.08, vmax=0.0, cmap="viridis", xticklabels=int(time/10),
                yticklabels=5, cbar_kws={'label': "Membrane Potential (V)"}, ax=ax)
    plt.xlabel("Time (ms)")
    plt.ylabel("# of neuron")
    plt.subplots_adjust(left=0.07, bottom=0.07, right=0.97, top=0.90)

    labels = [item.get_text() for item in ax.get_yticklabels()]

    for i, l in enumerate(labels):
        if int(l) in fixed_points:
            labels[i] = labels[i] + '\nFP'

    ax.set_yticklabels(labels)

    ax.set_title("Noise: {:.2E}\nWeights: {}\nError: {}\nVar of median: {}".format(
        noise, weights, round(error, 2), round(var_of_medians, 2)))

    plt.savefig(
        f"images/{datetime.now().strftime('%d-%m-%Y, %H:%M:%S')}.png")
    plt.show()


def see_neurons(A, ax, ratio_observed=1, arrows=True):
    """
    Visualizes the connectivity matrix.

    Args:
        A (np.ndarray): the connectivity matrix of shape (n_neurons, n_neurons)
        ax (plt.axis): the matplotlib axis to display on

    Returns:
        Nothing, but visualizes A.
    """
    n = len(A)

    ax.set_aspect('equal')
    thetas = np.linspace(0, np.pi * 2, n, endpoint=False)
    x, y = np.cos(thetas), np.sin(thetas),
    if arrows:
        for i in range(n):
            for j in range(n):
                if A[i, j] > 0:
                    ax.arrow(x[i], y[i], x[j] - x[i], y[j] - y[i], color='k', head_width=.05,
                             width=A[i, j] / 25, shape='right', length_includes_head=True,
                             alpha=.2)
    if ratio_observed < 1:
        nn = int(n * ratio_observed)
        ax.scatter(x[:nn], y[:nn], c='r', s=150, label='Observed')
        ax.scatter(x[nn:], y[nn:], c='b', s=150, label='Unobserved')
        ax.legend(fontsize=15)
    else:
        ax.scatter(x, y, c='k', s=150)
    ax.axis('off')
