import pandas as pd



#initial setting
df = pd.read_csv("sp500_features.csv", index_col = 0, parse_dates=True)
df = df.dropna(subset=['drawdown'])

df['regime_next'] = df['regime'].shift(-1)
df = df.dropna(subset=['regime_next'])
df['same_regime'] = df['regime'] == df['regime_next']
print("base line accuracy: ")
print(df['same_regime'].mean())



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
for train_idx, test_idx in splits:
    print(df.index[train_idx[0]], '→', df.index[train_idx[-1]], 
          '| test:', df.index[test_idx[0]], '→', df.index[test_idx[-1]])
    
for train_idx, test_idx in splits:
    test_df = df.iloc[test_idx]
    n_transitions = (~test_df['same_regime']).sum()
    print(df.index[test_idx[0]], '->', df.index[test_idx[-1]], '| transitions', n_transitions)
    
    
    
from sklearn.preprocessing import LabelEncoder
le = LabelEncoder()
df['regime_next_encoded'] = le.fit_transform(df['regime_next'])
print(le.classes_)
print(df['regime_next_encoded'].head())

features_cols = ['returns', 'vol', 'price', 'mom_5', 'mom_21', 'drawdown']

from sklearn.metrics import accuracy_score, confusion_matrix
from sklearn.metrics import precision_score, recall_score






#start
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import precision_score, recall_score

results = []

for fold_num, (train_idx, test_idx) in enumerate(splits):
    x_train = df.iloc[train_idx][features_cols]
    y_train = df.iloc[train_idx]['regime_next_encoded']
    x_test = df.iloc[test_idx][features_cols]
    y_test = df.iloc[test_idx]['regime_next_encoded']

    model = RandomForestClassifier(n_estimators=100, class_weight='balanced', random_state=42)
    model.fit(x_train, y_train)
    y_pred = model.predict(x_test)

    acc = accuracy_score(y_test, y_pred)

    actual_changed = ~df.iloc[test_idx]['same_regime']
    today_regime_encoded = le.transform(df.iloc[test_idx]['regime'])
    predicted_changed = (y_pred != today_regime_encoded)

    rec = recall_score(actual_changed, predicted_changed)
    prec = precision_score(actual_changed, predicted_changed)
    
    results.append({'fold': fold_num, 'accuracy': acc, 'recall': rec, 'precision': prec})
    print(f"Fold {fold_num}: acc= {acc:.3f}, recall={rec:.3f}, precision={prec:.3f}")

results_df = pd.DataFrame(results)
print(results_df)
print(results_df[['accuracy', 'recall', 'precision']].mean())



"""
#look at feature importances

importances_list = []

for fold_num, (train_idx, test_idx) in enumerate(splits):
    x_train = df.iloc[train_idx][features_cols]
    y_train = df.iloc[train_idx]['regime_next_encoded']

    model = RandomForestClassifier(n_estimators=100, class_weight='balanced', random_state=42)
    model.fit(x_train, y_train)

    importances = pd.Series(model.feature_importances_, index=features_cols)
    importances_list.append(importances)
    print(f"Fold {fold_num}:")
    print(importances.sort_values(ascending=False))
    print()

importances_df = pd.DataFrame(importances_list)
print("Average across folds:")
print(importances_df.mean().sort_values(ascending=False))
print(len(importances_list))


"""