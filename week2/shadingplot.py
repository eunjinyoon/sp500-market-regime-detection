import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("sp500_features.csv", index_col=0, parse_dates=True)
df = df.dropna(subset=["regime"])


#Color map for regimes
regime_colors = {
    "Calm": "lightgreen",
    "Normal": "lightyellow",
    "Elevated": "lightsalmon",
    "Crisis": "lightcoral"
}

fig, ax = plt.subplots(figsize=(14,6))

#Plot price
ax.plot(df.index, df["price"], color="black", linewidth=0.8, label="S&P 500")

#Shade regimes
prev_regime = None
start_idx = None

for i, (date, row) in enumerate(df.iterrows()):
    if row["regime"] != prev_regime:
        if prev_regime is not None:
            ax.axvspan(start_idx, date, alpha=0.3, color=regime_colors[prev_regime], label = prev_regime)
        start_idx = date
        prev_regime = row["regime"]

#Final segment
ax.axvspan(start_idx, df.index[-1], alpha=0.3, color=regime_colors[prev_regime], label=prev_regime)

#Remove duplicate legend entries
handles, labels = ax.get_legend_handles_labels()
by_label = dict(zip(labels, handles))
ax.legend(by_label.values(), by_label.keys())

ax.set_title("S&P 500 Price with Market Regime Shading")
ax.set_xlabel("Date")
ax.set_ylabel("Price")
plt.tight_layout()
plt.savefig("regime_shading.png", dpi=150)
plt.show()
    