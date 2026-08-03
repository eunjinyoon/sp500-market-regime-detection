import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("sp500_features.csv", index_col = 0, parse_dates=True)
df = df.dropna(subset=['drawdown'])

fig, ax = plt.subplots(figsize = (14, 6))
ax.plot(df.index, df["drawdown"], color="blue", linewidth = 0.8, label="drawdown")

regimes_color = {
    "Calm": "lightgreen",
    "Normal": "lightyellow",
    "Elevated": "lightsalmon",
    "Crisis": "lightcoral"
}

prev_regime = None
start_idx = None

for i, (date, row) in enumerate(df.iterrows()):
    if row["regime"] != prev_regime:
        if prev_regime is not None:
            ax.axvspan(start_idx, date, alpha=0.3,  color=regimes_color[prev_regime], label = prev_regime)
        start_idx = date
        prev_regime = row["regime"]

ax.axvspan(start_idx, df.index[-1], alpha=0.3, color=regimes_color[prev_regime], label=prev_regime)


#Remove duplicate legend entries
handles, labels = ax.get_legend_handles_labels()
by_label = dict(zip(labels, handles))
ax.legend(by_label.values(), by_label.keys())

ax.set_title("S&P 500 drawdown by regimes")
ax.set_xlabel("date")
ax.set_ylabel("drawdown")
plt.savefig("drawdown_regimes.png")
plt.show()
