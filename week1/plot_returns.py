import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

data = yf.download("^GSPC", start = "2015-01-01")
close = data["Close"]
returns = close.pct_change()

plt.figure(figsize=(12,5))
plt.plot(returns)
plt.title("S&P 500 Daily Returns (2015-now)")
plt.xlabel("Date")
plt.ylabel("Daily Return")
plt.axhline(0, color = "black", linewidth = 0.5)
plt.show()
