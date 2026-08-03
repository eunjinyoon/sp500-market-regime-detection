import yfinance as yf
import pandas as ad
import numpy as np

#데이터 받아오기
data = yf.download("^GSPC", start = "2015-01-01")

#종가만 꺼내기
close = data["Close"]

returns = close.pct_change()

print(returns.head())
print(returns.describe())
