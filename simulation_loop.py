import numpy as np
import pandas as pd
from tqdm import tqdm
from ring_attractor import RingAttractor
from utils import calculate_weights

if __name__ == "__main__":

    weights = [0.050, 0.088, 0.050, 0.095]  # ext, inh, fp ext, inh
    fixed_points = [0, 1, 2, 4, 8, 16, 32]
    time = 5000
    iterations = 20
    noise_levels = 5

    noises = np.linspace(0.0e-3, 2.0e-3, noise_levels)
    fixed_points_idx = [str(i) for i in fixed_points]
    noises_idx = ["{:.2E}".format(i) for i in noises]

    records = pd.DataFrame(index=fixed_points_idx, columns=noises_idx)

    for n_idx, noise in tqdm(zip(noises_idx, noises)):
        for fp_idx, fp_n in zip(fixed_points_idx, fixed_points):

            errors = []
            for _ in range(iterations):
                ring = RingAttractor(noise=noise, weights=calculate_weights(
                    weights, fp_n), fixed_points_number=fp_n)
                e = ring.simulate(time=time)

                if not np.isnan(e):
                    errors.append(e)

            records.loc[fp_idx, n_idx] = np.mean(errors)

    records.to_csv("error_by_noise.csv")
