import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("sp500_features.csv", index_col=0, parse_dates=True)
df = df.dropna(subset=["vol"])


fig, ax = plt.subplots(figsize=(14,6))
ax.plot(df.index, df["vol"], color="black", linewidth=0.8, label="vol_21")

ax.axhline(y=0.13, color='blue', linestyle='dashed', label='0.13')
ax.axhline(y=0.18, color='green', linestyle='dashed', label='0.18')
ax.axhline(y=0.24, color='orange', linestyle='dashed', label='0.24')

ax.set_title("S&P 500 volatility")
ax.set_xlabel("date")
ax.set_ylabel("vol_21")
ax.legend()
plt.tight_layout()
plt.savefig("rolling_volatility.png", dpi=150)
plt.show()
