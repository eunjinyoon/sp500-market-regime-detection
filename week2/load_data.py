import pandas as pd

df = pd.read_csv("sp500_regimes.csv", index_col = 0, parse_dates=True)
print(df.head())
print(df.shape)