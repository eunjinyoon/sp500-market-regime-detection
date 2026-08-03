import yfinance as yf
import pandas as pd
import numpy as np

#Get data, compute returns, then rolling volatility
data = yf.download("^GSPC", start="2015-01-01")
close = data["Close"]
returns = close.pct_change()
rolling_vol = returns.rolling(window=21).std() * np.sqrt(252)

#Summary statistics of the rolling volatility itself
print(rolling_vol.describe())

#Specific percentiles
print("\nPercentiles:")
print(rolling_vol.quantile([0.25, 0.5, 0.75, 0.90, 0.95, 0.99]))