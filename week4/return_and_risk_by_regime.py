
#%%

import pandas as pd
import matplotlib.pyplot as plt
import math
from scipy.stats import kurtosis

df = pd.read_csv("sp500_features.csv")
groups = df.groupby("regime")[['returns']].agg(['mean', 'std', 'count', 'skew'])

groups['kurt'] = df.groupby("regime")['returns'].apply(kurtosis)

groups.columns = groups.columns.droplevel(0)

groups['sharpe'] = groups['mean'] / groups['std'] * math.sqrt(252)


regime_order = ['Calm','Normal','Elevated','Crisis'] 
data_to_plot = [df[df['regime']==regime]["returns"] for regime in regime_order]

"""
plt.figure(figsize=(10,6))
plt.boxplot(data_to_plot, labels=regime_order)
plt.title('Return Distribution by Regime')
plt.ylabel('Daily Return')
plt.xlabel('Regime')
plt.grid(True, alpha=0.3)
plt.savefig('regime_boxplot.png')
plt.show()
"""

print("test")


#Anova test: whether mean returns differ across regimes

from scipy.stats import f_oneway


f_stat, p_value = f_oneway(data_to_plot[0], data_to_plot[1], data_to_plot[2], data_to_plot[3])
print(f"F-statistic: {f_stat:.4f}")
print(f"P-value: {p_value:.4f}")

plt.show()
# %%
