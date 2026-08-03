import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats

df = pd.read_csv("sp500_features.csv")
df = df.dropna(subset=['regime'])

#ANOVA test (mean returns)
groups = [group["returns"].values for name, group in df.groupby("regime")]
f_stat, p_value = stats.f_oneway(*groups)
print(f"F-statistic: {f_stat:.4f}")
print(f"P-value: {p_value:.4f}")

#Levene's test (variance)
levene_stat, levene_p = stats.levene(*groups)
print(f"Levene F-statistic: {levene_stat:.4f}")
print(f"Levene P-value: {levene_p:.4f}")

#Kruskal-Wallis test (whether the full distributions differ across regimes)
kruskal_stat, kruskal_p = stats.kruskal(*groups)
print(f"Kruskal-Wallis statistic: {kruskal_stat:.4f}")
print(f"Kruskal-Wallis P-value: {kruskal_p:.4f}")


#pairwise t-tests
from itertools import combinations

regimes = ["Calm", "Normal", "Elevated", "Crisis"]

for r1, r2 in combinations(regimes, 2):
    g1 = df[df["regime"]==r1]["returns"].values
    g2 = df[df["regime"]==r2]["returns"].values
    stat, p = stats.levene(g1,g2)
    print(f"{r1} vs {r2}: p = {p:.4f}")

    
#return distribution plots to visualize the statistical results
data = [df[df["regime"]==r]["returns"].values for r in regimes]

fig, ax = plt.subplots(figsize=(8,5))
ax.boxplot(data, labels=regimes)
ax.axhline(0, color="black", linestyle="--", linewidth=0.8)
ax.set_title("Return Distribution by Regime")
ax.set_xlabel("Regime")
ax.set_ylabel("Daily return ")
plt.tight_layout()
plt.savefig("return_distribution.png", dpi=150)
plt.show()