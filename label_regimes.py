import yfinance as yf
import pandas as pd
import numpy as np

#Get data, returns, rolling vol
data = yf.download("^GSPC", start="2015-01-01")
close = data["Close"]
returns = close.pct_change()
rolling_vol = returns.rolling(window=21).std() * np.sqrt(252)

#Combine into one Dataframe for convenience
df = pd.DataFrame({
    "returns": returns.squeeze(),
    "vol": rolling_vol.squeeze()
})

#Assign a regime label to each day based on volatility
def assign_regime(v):
    if pd.isna(v):
        return np.nan
    elif v < 0.13:
        return "Calm"
    elif v < 0.18:
        return "Normal"
    elif v < 0.24:
        return "Elevated"
    else:
        return "Crisis"

df["regime"] = df["vol"].apply(assign_regime)

#How many days fell into each regime?
print("Days per regime:")
print(df["regime"].value_counts())

#what do returns look like inside each regime?
print("\nReturn statistics by regime:")
print(df.groupby("regime")["return"].describe())