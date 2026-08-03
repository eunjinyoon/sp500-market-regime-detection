import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats

df = pd.read_csv("sp500_features.csv")

df["fwd_return_5"] = df["returns"].shift(-5).rolling(5).sum()
df["fwd_return_21"] = df["returns"].shift(-21).rolling(21).sum()
df = df.dropna(subset=['regime', 'fwd_return_5', 'fwd_return_21'])

groups = df.groupby("regime")[["fwd_return_5", "fwd_return_21"]].agg(["mean", "std"])


#testing whether crisis regime has risk premium
crisis_test = df[df["regime"]=="Crisis"]["fwd_return_21"]
elevated_test = df[df["regime"]=="Elevated"]["fwd_return_21"]
ttest_stat, ttest_p = stats.ttest_ind(crisis_test, elevated_test)
print(ttest_p)

df["episode_id"] = (df["regime"] != df["regime"].shift(1)).cumsum()
episodes = df.groupby("episode_id").agg(
    regime = ("regime", "first"),
    duration = ("regime", "count")
)

df = df.merge(episodes[["duration"]], on="episode_id")

groups = df.groupby("regime")[["duration", "fwd_return_21"]].corr()
print(groups)