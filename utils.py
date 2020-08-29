from datetime import datetime
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression

# TODO: explore parameters of this function
def calculate_weights(weights, fp_n=16, total_neurons=128):
    if fp_n >= 1:
        new_weights = [0, 0, 0, 0]
        new_weights[0] = 0.9 * weights[0]
        new_weights[1] = 0.9 * weights[1]
        new_weights[2] = (0.1 * total_neurons/fp_n + 1) * weights[0]
        new_weights[3] = (0.1 * total_neurons/fp_n + 1) * weights[1]
    else:
        new_weights = weights
    return new_weights


def circular_mean(angles): 
      a = np.array(angles) * np.pi / 180.  
      s = np.nanmean(np.sin(a)) 
      c = np.nanmean(np.cos(a)) 
       
      if c < 0 and s > 0: 
          return np.arctan(s/c) * 180. / np.pi + 180 
      elif s < 0 and c > 0: 
          return np.arctan(s/c) * 180. / np.pi + 360 
      else: 
          return np.arctan(s/c) * 180. / np.pi 

def plot_errors(csv_name):
    _, ax = plt.subplots(figsize=(10, 10))
    df = pd.read_csv(csv_name, index_col=0)
    sns.barplot(df.index, df.errors, ax=ax, palette=sns.cubehelix_palette(8))

    ax.set_ylabel("Absolute Error")
    ax.set_xlabel("# of Fixed Points")
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    plt.savefig("errors.png")
    plt.show()
