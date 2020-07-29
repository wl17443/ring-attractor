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

    weights = [0.025, 0.05, 0.090, 0.3]  # ext, inh, fp ext, inh
    error, var = simulate(weights, fp_n=0, noise=2e-3)

    fixed_points = [2, 4, 8, 16, 32, 64, 128]
    noises = np.linspace(2e-3, 2.3e-3, num=20)

    records = pd.DataFrame(index=fixed_points, columns = noises)
    var_records = pd.DataFrame(index=fixed_points, columns = noises)

    for n in tqdm(noises):
        for i in fixed_points:
            errors = []
            variances = []

            for _ in range(10):
                e, v = simulate(weights, fp_n=i, noise=n)
                errors.append(e)
                variances.append(v)

            records.loc[i, n] = np.mean(errors)
            var_records.loc[i, n] = np.mean(variances)


    records.to_csv("error_by_noise.csv", index=False)
    var_records.to_csv("var_by_noise.csv", index=False)



