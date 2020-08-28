import concurrent.futures 
import numpy as np
import pandas as pd
from tqdm import tqdm
from ring_attractor import RingAttractor
from utils import calculate_weights

weights = [0.050, 0.088, 0.050, 0.25]  # ext, inh, fp ext, inh
fixed_points = [0, 1, 2, 4, 8, 16, 32]
time = 10000
iterations = 30
noise_levels = 30
neurons_n = 256

noises = np.linspace(0.0e-3, 3.0e-3, noise_levels)
fixed_points_idx = [str(i) for i in fixed_points]
noises_idx = ["{:.2E}".format(i) for i in noises]

records = pd.DataFrame(index=fixed_points_idx, columns=noises_idx)


def iteration(_noise, _fp_n): 
    ring = RingAttractor(n=neurons_n, noise=_noise, weights=weights, fixed_points_number=_fp_n, time=time)
    e = ring.simulate()

    return e

for n_idx, noise in tqdm(zip(noises_idx, noises)):
    for fp_idx, fp_n in zip(fixed_points_idx, fixed_points):

        errors = []
        with concurrent.futures.ProcessPoolExecutor() as executor:
            results = [executor.submit(iteration, noise, fp_n) for _ in range(iterations)]

            for f in concurrent.futures.as_completed(results):
                errors.append(f.result())


        records.loc[fp_idx, n_idx] = np.mean(errors)

    records.to_csv("error_by_noise.csv")


