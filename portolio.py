import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


#initial setting
df = pd.read_csv("sp500_features.csv", index_col = 0, parse_dates=True)
df = df.dropna(subset=['drawdown'])

df["rolling_vol"] = df['returns'].rolling(window=21).std() * np.sqrt(252)




#benchmark A
target_volatility = df[df["regime"]=="Calm"]["rolling_vol"].mean()
df["weight_equity_t"] = target_volatility / df["rolling_vol"]
df["weight_equity_t"] = df["weight_equity_t"].clip(upper=1)
df["weight_equity_t"] = df["weight_equity_t"].shift(1)

df["portfolio_return_t"] = df["weight_equity_t"] * df["returns"] + (1 - df["weight_equity_t"]) * 0 #cash return

df = df.dropna(subset = "portfolio_return_t")
df["benchmark_return_t"] = df["returns"]
df["cum_strategy"] = (1 + df["portfolio_return_t"]).cumprod()
df["cum_benchmark"] = (1+ df["benchmark_return_t"]).cumprod()

"""
print(df[["portfolio_return_t", "benchmark_return_t", "cum_strategy", "cum_benchmark"]].tail())


fig = plt.figure(figsize=(14,6))
ax = fig.add_subplot(1, 1, 1)
ax.plot(df["cum_strategy"], label = "cum_strategy")
ax.plot(df["cum_benchmark"], label = "cum_benchmark")
ax.set(xlabel = "date", ylabel = "cum strategy/benchmark", title = "cum strategy/benchmark comparison")

plt.legend()
plt.show()

"""


running_peak = df["cum_strategy"].cummax()
df["drawdown_strategy"] = (df["cum_strategy"] - running_peak) / running_peak

running_peak = df["cum_benchmark"].cummax()
df["drawdown_benchmark"] = (df["cum_benchmark"] - running_peak) / running_peak

max_dd_strategy = df["drawdown_strategy"].min()
max_dd_benchmark = df["drawdown_benchmark"].min()

print("test")
print(f"max drawdown strategy: {max_dd_strategy:.3f}, max drawdown benchmark: {max_dd_benchmark:.3f}")

sharpe_strategy = df["portfolio_return_t"].mean() / df["portfolio_return_t"].std() * np.sqrt(252)
sharpe_benchmark = df["benchmark_return_t"].mean() / df["benchmark_return_t"].std() * np.sqrt(252)
print(f"sharpe strategy: {sharpe_strategy:.3f}, sharpe benchmark{sharpe_benchmark:.3f}")





#benchmark B - regression model
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import LabelEncoder
le = LabelEncoder()

features_cols = ['returns', 'vol', 'price', 'mom_5', 'mom_21', 'drawdown']


def walk_forward_splits(df, n_folds, test_size, embargo, initial_train) :
    n = len(df)
    splits = []
    train_end = initial_train
    
    for i in range(n_folds):
        test_start = train_end + embargo
        test_end = test_start + test_size

        if test_end > n:
            break
        
        train_idx = range(0, train_end)
        test_idx = range(test_start, test_end)

        splits.append((train_idx, test_idx))
        
        train_end += test_size
        
    return splits

splits = walk_forward_splits(df, n_folds=5, test_size=150, embargo=20, initial_train=1000)
df['regime_next'] = df['regime'].shift(-1)
df['regime_next_encoded'] = le.fit_transform(df['regime_next'])




df["regime_next_pred_encoded"] = np.nan

results = []

for fold_num, (train_idx, test_idx) in enumerate(splits):
    x_train = df.iloc[train_idx][features_cols]
    y_train = df.iloc[train_idx]['regime_next_encoded']
    x_test = df.iloc[test_idx][features_cols]
    y_test = df.iloc[test_idx]['regime_next_encoded']

    scaler = StandardScaler()
    x_train_scaled = scaler.fit_transform(x_train)
    x_test_scaled = scaler.transform(x_test)
    
    model = LogisticRegression(max_iter = 10000)
    model.fit(x_train_scaled, y_train)
    y_pred = model.predict(x_test_scaled)
    
    df.iloc[test_idx, df.columns.get_loc("regime_next_pred_encoded")] = y_pred

results_df = pd.DataFrame(results)


mask = df["regime_next_pred_encoded"].notna()
df.loc[mask, "regime_next_pred"] = le.inverse_transform(
    df.loc[mask, "regime_next_pred_encoded"].astype(int)
)

regime_vol_map = df.groupby("regime")["rolling_vol"].mean()
df["predicted_vol"] = df["regime_next_pred"].map(regime_vol_map)


# allocation pipeline
df["weight_equity_t_B"] = target_volatility / df["predicted_vol"]
df["weight_equity_t_B"] = df["weight_equity_t_B"].clip(upper=1)
df["weight_equity_t_B"] = df["weight_equity_t_B"].shift(1)

df["portfolio_return_t_B"] = df["weight_equity_t_B"] * df["returns"] + (1 - df["weight_equity_t_B"]) * 0

print(df[["portfolio_return_t_B", "benchmark_return_t"]].dropna().head())


#comparing A and B
test_fold_dates = df["portfolio_return_t_B"].dropna().index

df.loc[test_fold_dates, "cum_strategy_A_sliced"] = (1 + df.loc[test_fold_dates, "portfolio_return_t"]).cumprod()
df.loc[test_fold_dates, "cum_benchmark_sliced"] = (1 + df.loc[test_fold_dates, "benchmark_return_t"]).cumprod()
df.loc[test_fold_dates, "cum_strategy_B"] = (1 + df.loc[test_fold_dates, "portfolio_return_t_B"]).cumprod()

a = df.loc[test_fold_dates, "cum_strategy_A_sliced"]
b = df.loc[test_fold_dates, "cum_strategy_B"]
bench = df.loc[test_fold_dates, "cum_benchmark_sliced"]

max_dd_strategy_A = ((a - a.cummax()) / a.cummax()).min()
max_dd_strategy_B = ((b - b.cummax()) / b.cummax()).min()
max_dd_benchmark  = ((bench - bench.cummax()) / bench.cummax()).min()

sharpe_A = df.loc[test_fold_dates, "portfolio_return_t"].mean() / df.loc[test_fold_dates, "portfolio_return_t"].std() * np.sqrt(252)
sharpe_B = df["portfolio_return_t_B"].mean() / df["portfolio_return_t_B"].std() * np.sqrt(252)
sharpe_bench = df.loc[test_fold_dates, "benchmark_return_t"].mean() / df.loc[test_fold_dates, "benchmark_return_t"].std() * np.sqrt(252)

print(f"Max DD  — A: {max_dd_strategy_A:.3f} | B: {max_dd_strategy_B:.3f} | Benchmark: {max_dd_benchmark:.3f}")
print(f"Sharpe  — A: {sharpe_A:.3f} | B: {sharpe_B:.3f} | Benchmark: {sharpe_bench:.3f}")