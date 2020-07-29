import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from datetime import datetime
from tqdm import tqdm
from connect import connect_with_fixed_points
from lif_model import LIF
from ring_attractor import simulate


if __name__ == "__main__":


    weights = [0.035, 0.088, 0.050, 0.095]  # ext, inh, fp ext, inh RIGHT WEIGHTS FOR 32 FP
    starting points = [44, 40, 46, 32]
    fixed_points = [2, 4, 8, 16]
    noises = np.linspace(2e-3, 3e-3, num=10)

    records = pd.DataFrame(index=fixed_points, columns = noises)
    var_records = pd.DataFrame(index=fixed_points, columns = noises)

    for n in tqdm(noises):
        for n, fp in fixed_points:
            errors = []
            variances = []

            for _ in range(10):
                e, v = simulate(weights,
                                fp_n=fp,
                                noise=n,
                                starting_point=starting_points[i])

                errors.append(e)
                # variances.append(v)

            records.loc[i, n] = np.mean(errors)
            # var_records.loc[i, n] = np.mean(variances)


    records.to_csv("error_by_noise.csv", index=False)
    var_records.to_csv("var_by_noise.csv", index=False)



