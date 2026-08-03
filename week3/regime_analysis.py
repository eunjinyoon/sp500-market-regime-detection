import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("sp500_features.csv")
df = df.dropna(subset=['regime'])


df["episode_id"] = (df["regime"] != df["regime"].shift(1)).cumsum()
selected = ["Date", "regime", "episode_id"]



episodes = df.groupby("episode_id").agg(
    regime=("regime", "first"),
    duration=("regime", "count")
)



duration_stats = episodes.groupby("regime")["duration"].agg(
    count="count",
    mean="mean",
    median="median",
    max="max"
).round(1)


df["next_regime"] = df["regime"].shift(-1)

transitions = pd.crosstab(
    df["regime"],
    df["next_regime"],
    normalize="index"
).round(3)



import numpy as np

regime_order = ["Calm", "Normal", "Elevated", "Crisis"]
matrix = transitions.loc[regime_order, regime_order]

fig, ax = plt.subplots(figsize=(7,5))
im = ax.imshow(matrix.values, cmap="YlOrRd")

ax.set_xticks(range(4))
ax.set_yticks(range(4))
ax.set_xticklabels(regime_order)
ax.set_yticklabels(regime_order)
ax.set_xlabel("Next Regime")
ax.set_ylabel("Current Regime")
ax.set_title("Regime Transition Probability Matrix")

for i in range(4):
    for j in range(4):
        ax.text(j, i, f"{matrix.values[i,j]:.3f}",
                ha="center", va="center", fontsize=10)
        
plt.colorbar(im, ax=ax)
plt.tight_layout()
plt.savefig("transition_matrix.png", dpi=150)
plt.show()
        