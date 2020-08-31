import concurrent.futures
import numpy as np
import pandas as pd
from utils import Counter
from ring_attractor import RingAttractor


# params = {
#     "neurons_n": 256,
#     "simulation_time": 10000,
#     "iterations": 30,
#     "noise_levels": 30,
#     "noise_low": 0.0,
#     "noise_high": 3.0e-3,
#     "weights": [0.050, 0.100, 0.050, 0.250],  # ext, inh, fp ext, inh
#     "fixed_points": [0, 1, 2, 4, 8, 16, 32]
# }

# Dummy params
params = {
    "neurons_n": 32,
    "simulation_time": 100,
    "iterations": 2,
    "noise_levels": 3,
    "noise_low": 0.0,
    "noise_high": 3.0e-3,
    "weights": [0.050, 0.100, 0.050, 0.250],  # ext, inh, fp ext, inh
    "fixed_points": [0, 1, 2]
}


def simulation(parameters, _noise, noise_idx, _fp_n, fp_idx, it_n, counter):

    ring = RingAttractor(n=parameters["neurons_n"],
                         noise=_noise,
                         weights=parameters["weights"],
                         fixed_points_number=_fp_n,
                         time=parameters["simulation_time"],
                         random_seed=seeds[it_n])

    e = ring.simulate()
    counter.inc()

    return e, noise_idx, fp_idx, it_n


noises = np.linspace(
    params["noise_low"], params["noise_high"], params["noise_levels"])
noises_idx = ["{:.2e}".format(i) for i in noises]
fixed_points_idx = [str(i) for i in params["fixed_points"]]

records = [pd.DataFrame(index=fixed_points_idx, columns=noises_idx)
           for _ in range(params["iterations"])]
seeds = np.random.choice(10000, params["iterations"])
counter = Counter(params)
results = []


with concurrent.futures.ThreadPoolExecutor() as executor:

    for it in range(params["iterations"]):
        for noise_idx, noise in zip(noises_idx, noises):
            for fp_idx, fp_n in zip(fixed_points_idx, params["fixed_points"]):

                results.append(executor.submit(
                    simulation, params, noise, noise_idx, fp_n, fp_idx, it, counter))


for f in concurrent.futures.as_completed(results):
    error, noise_idx, fp_idx, it_n = f.result()
    records[it_n].loc[fp_idx, noise_idx] = error

for i, df in enumerate(records):
    df.to_csv("csv/errors_seed_{}.csv".format(seeds[i]))
    # TODO take mean across all records
