import pandas as pd

df = pd.read_csv("sp500_features.csv", index_col=0, parse_dates=True)
df = df.dropna(subset=['drawdown'])

# t+5 target - changes in shift amounts
df['regime_next_5'] = df['regime'].shift(-5)
df = df.dropna(subset=['regime_next_5'])
df['same_regime_5'] = df['regime'] == df['regime_next_5']
print("baseline accuracy (t+5): ")
print(df['same_regime_5'].mean())




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

from sklearn.preprocessing import LabelEncoder
le = LabelEncoder()
de['regime_next_5_encoded'] = le.fit_transform(df['regime_next_5'])
print(le.classes_)

features_cols = ['returns', 'vol', 'price', 'mom_5', 'mom_21', 'drawdown']

