import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("sp500_features.csv", index_col = 0, parse_dates=True)
df = df.dropna(subset=["regime"])

fig, axs = plt.subplots(1, 4, figsize=(14,6), sharey=True, sharex=True)

regimes = ["Calm", "Normal", "Elevated", "Crisis"]

for i , regime in enumerate(regimes):
    data = df[df["regime"] == regime]
    axs[i].hist(data["returns"])
    axs[i].set_title(regime)
    

plt.tight_layout()
plt.savefig("regime_distributions.png")
plt.show()