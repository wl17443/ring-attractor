import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from datetime import datetime
from connect import connect_with_fixed_points
from lif_model import LIF


#   python C:\Users\Nikitas\Desktop\NEW\CODE\ring_attractor.py

import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from datetime import datetime
from connect import connect_with_fixed_points
from lif_model import LIF

time = 600
n = 128
weights = [0.045, 0.1, 0.060, 0.2]  # ext, inh, fp ext, inh
dt = 1
spike_source = [c for c in range(40, 45)]

neurons = [LIF(ID, dt=dt, noise_mean=0, noise_std=0e-3) for ID in range(n)]


fixed_points = connect_with_fixed_points(neurons, n, weights, fp_n=8)
print(fixed_points)

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
fig, ax = plt.subplots(figsize=(10,10))

df = pd.DataFrame(potentials)
sns.heatmap(df, vmin=-0.08, vmax=0.0, cmap="viridis", xticklabels=int(time/10), yticklabels=5, cbar_kws={'label':"Membrane Potential (V)"}, ax=ax)
plt.xlabel("Time (ms)")
plt.ylabel("# of neuron")
plt.subplots_adjust(left=0.07, bottom=0.07, right=0.97, top=0.95)

labels = [item.get_text() for item in ax.get_yticklabels()]

for i, l in enumerate(labels):
    if int(l) in fixed_points:
        labels[i] = labels[i] + '\nFP'

ax.set_yticklabels(labels)


plt.savefig(f"images/{datetime.now().strftime('%d-%m-%Y, %H-%M-%S')}.png")
plt.show()