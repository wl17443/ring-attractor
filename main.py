import numpy as np
import pandas as pd
from tqdm import tqdm
from Ring_Attractor import simulate


def calculate_weights(weights, fp_n=16,total_neurons = 128):
    if fp_n>=1:
        new_weights = [0, 0, 0, 0]
        new_weights[0] = 0.9*weights[0]
        new_weights[1] = 0.9*weights[1]
        new_weights[2] = (0.1*total_neurons/fp_n + 1)*weights[0]
        new_weights[3] = (0.1*total_neurons/fp_n + 1)*weights[1]
    else:
        new_weights = weights   
    return new_weights

if __name__ == "__main__":


    weights = [0.050, 0.088, 0.050, 0.095]  # ext, inh, fp ext, inh RIGHT WEIGHTS FOR 32 FP

    starting_points = [50, 50, 44, 40, 46, 32, 46]

    fixed_points = [0, 1, 2, 4, 8, 16, 32]

    noises = np.linspace(2e-3, 3e-3, num=10)
    fixed_points_idx = [str(i) for i in fixed_points]
    noises_idx = ["{:.2E}".format(i) for i in noises]

    records = pd.DataFrame(index=fixed_points_idx, columns=["errors"])
    # var_records = records.copy()

    # for n_idx, n in tqdm(enumerate(noises)):
    for i, fp in enumerate(fixed_points):
        errors = []
        # variances = []

        for _ in range(2):
            e, _ = simulate(calculate_weights(weights, fp),
                            fp_n=fp,
                            noise=2.5e-3,
                            starting_point=starting_points[i])

            if not np.isnan(e):
                errors.append(e)
            # variances.append(v)

        
        records.loc[fixed_points_idx[i], "errors"] = np.mean(errors)
        # var_records.loc[i, n] = np.mean(variances)


    records.to_csv("error_by_noise_weights.csv")
    # var_records.to_csv("var_by_noise.csv")

