import pandas as pd
import matplotlib.pyplot as plt
import yfinance as yf

df = pd.read_csv("sp500_features.csv")
df = df.set_index("Date")
df.index = pd.to_datetime(df.index)

gs = yf.download("GS", start="2015-01-01")
gs['gs_returns'] = gs['Close'].pct_change()

df_gs = pd.merge(df, gs['gs_returns'], left_index = True, right_index=True)


import statsmodels.formula.api as smf

model = smf.ols("gs_returns ~ returns", data = df_gs)
results = model.fit()

"""
for regime in ["Calm", "Normal", "Elevated", "Crisis"]:
    subset = df_gs[df_gs["regime"]==regime]
    test = smf.ols("gs_returns ~ returns", data = subset)
    results = test.fit()
    print(results.summary())
   """ 
    
    
#Fama-french
import pandas_datareader as pdr

ff_data = pdr.get_data_famafrench("F-F_Research_Data_Factors_daily", start = "2015-01-01")

df_gs_fama = df_gs.copy()
df_gs_fama["returns"] *= 100
df_gs_fama["gs_returns"] *= 100

df_gs_fama = pd.merge(df_gs_fama[["returns", "gs_returns", "regime"]], ff_data[0], left_index = True, right_index = True)
df_gs_fama = df_gs_fama.dropna(subset=["regime", "returns", "gs_returns"])
df_gs_fama = df_gs_fama.rename(columns={"Mkt-RF": "Mkt_RF"})

model = smf.ols("gs_returns ~ Mkt_RF + SMB + HML", data = df_gs_fama)
results = model.fit()

for regime in ["Calm", "Normal", "Elevated", "Crisis"]:
    subset = df_gs_fama[df_gs_fama["regime"] == regime]
    test = smf.ols("gs_returns ~ Mkt_RF + SMB + HML", data = subset)
    results = test.fit()
    print(results.summary())
