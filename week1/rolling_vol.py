import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

#Get data and compute returns (same as before)
data = yf.download("^GSPC", start = "2015-01-01")
close = data["Close"]
returns = close.pct_change()

#Rolling volatility: std of returns over a moving 21-day window
rolling_vol = returns.rolling(window=21).std()

#Annualize it
rolling_vol_annualized = rolling_vol * np.sqrt(252)

plt.figure(figsize=(12,5))
plt.plot(rolling_vol_annualized)
plt.title("S&P 500 Rolling Volatility(21-day window, annualized)")
plt.xlabel("Date")
plt.ylabel("Annualized Volatility")
plt.show()