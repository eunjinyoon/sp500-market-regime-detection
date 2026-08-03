import yfinance as yf
import pandas as pd

# S&P 500 지수 데이터 받아오기 (2015년부터 오늘까지)
data = yf.download("^GSPC", start="2015-01-01")

# 데이터가 어떻게 생겼는지 보기
print(data.head())      # 맨 위 5줄
print(data.shape)       # (행 개수, 열 개수)