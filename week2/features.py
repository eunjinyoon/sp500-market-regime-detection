import pandas as pd

df = pd.read_csv("sp500_regimes.csv", index_col = 0, parse_dates=True)

#Momentum: rolling mean return over 5 and 21 days
df["mom_5"] = df["returns"].rolling(window=5).mean()
df["mom_21"] = df["returns"].rolling(window=21).mean()

#Drawdown: how far price has dropped from its rolling peak
rolling_peak = df["price"].rolling(window=252).max()
df["drawdown"] = (df["price"] - rolling_peak) / rolling_peak
print(df[["returns", "mom_5", "mom_21", "drawdown"]].tail(10))

df.to_csv("sp500_features.csv")
