import concurrent.futures
import numpy as np
import pandas as pd
from ring_attractor import RingAttractor

### Parameters
neurons_n = 256
time = 100
iterations = 2

noise_levels = 15
noise_low = 0.0
noise_high = 1.5e-3

weights = [0.050, 0.100, 0.050, 0.250]  # ext, inh, fp ext, inh
fixed_points = [0, 1, 2, 4, 8, 16, 32]
###

noises = np.linspace(noise_low, noise_high, noise_levels)
noises_idx = ["{:.2E}".format(i) for i in noises]
fixed_points_idx = [str(i) for i in fixed_points]

records = [pd.DataFrame(index=fixed_points_idx, columns=noises_idx) for _ in noises]
results = []
seeds = np.random.choice(10000, iterations)


def iteration(_noise, noise_idx, _fp_n, fp_idx, it_n):
    ring = RingAttractor(n=neurons_n, noise=_noise, weights=weights, fixed_points_number=_fp_n, time=time, random_seed=seeds[it])
    e = ring.simulate()

    return e, noise_idx, fp_idx, it_n


if __name__ == "__main__":
    with concurrent.futures.ProcessPoolExecutor() as executor:

        for it in range(iterations):
            for n_idx, noise in zip(noises_idx, noises):
                for fp_idx, fp_n in zip(fixed_points_idx, fixed_points):
                    results.append(executor.submit(iteration, noise, n_idx, fp_n, fp_idx, it))


    for f in concurrent.futures.as_completed(results):
        error, noise_idx, fp_idx, it_n = f.result()
        records[it_n].loc[fp_idx, noise_idx] = error

    for i, df in enumerate(records):
        df.to_csv("csv/errors_it_{}_seed_{}.csv".format(i, seeds[i]))
        # TODO take mean across all records
