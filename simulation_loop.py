import concurrent.futures
import numpy as np
import pandas as pd
from ring_attractor import RingAttractor

neurons_n = 256
time = 100
iterations = 1

noise_levels = 15
noise_low = 0.0
noise_high = 1.5e-3

weights = [0.050, 0.100, 0.050, 0.250]  # ext, inh, fp ext, inh
fixed_points = [0, 1, 2, 4, 8, 16, 32]

noises = np.linspace(noise_low, noise_high, noise_levels)
noises_idx = ["{:.2E}".format(i) for i in noises]
fixed_points_idx = [str(i) for i in fixed_points]

records = [pd.DataFrame(index=fixed_points_idx, columns=noises_idx) for _ in noises]
seeds = records.copy()
results = []


def iteration(_noise, _fp_n, seed, ID):
    ring = RingAttractor(n=neurons_n, noise=_noise, weights=weights, fixed_points_number=_fp_n, time=time, random_seed=seed)
    e = ring.simulate()

    return e, noises_idx[ID], str(_fp_n), seed, ID


if __name__ == "__main__":
    with concurrent.futures.ProcessPoolExecutor() as executor:


        for i, noise in enumerate(noises):
            for fp_n in fixed_points:
                for _ in range(iterations):
                    results.append(executor.submit(iteration, noise, fp_n, np.random.choice(10000), i))


    for f in concurrent.futures.as_completed(results):
        error, noise_idx, fp_idx, seed, ID = f.result()
        records[ID].loc[fp_idx, noise_idx] = error
        seeds[ID].loc[fp_idx, noise_idx] = seed

    for i, df in records:
        df.to_csv("errors_it_{}.csv".format(i))

    for i, df in seeds:
        df.to_csv("seeds_it_{}.csv".format(i))
