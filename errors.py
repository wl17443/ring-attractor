import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt

fig, ax = plt.subplots(figsize=(10,10))
df = pd.read_csv("error_by_noise_weights.csv", index_col=0)
sns.barplot(df.index, df.errors, ax=ax, palette=sns.cubehelix_palette(8))

ax.set_ylabel("Absolute Error")
ax.set_xlabel("# of Fixed Points")
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
plt.savefig("errors.png")
plt.show()

