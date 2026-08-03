import pandas as pd

df = pd.read_csv("sp500_features.csv", index_col = 0, parse_dates=True)
df = df.dropna(subset=['drawdown'])

df['regime_next'] = df['regime'].shift(-1)
df = df.dropna(subset=['regime_next'])
df['same_regime'] = df['regime'] == df['regime_next']
print("base line accuracy: ")
print(df['same_regime'].mean())

df_filtered = df[df['regime']=='Crisis']
print(df_filtered.head())
print(df_filtered.index.min())
print(df_filtered.index.max())
print(len(df_filtered))

n_folds = 5
test_size = 150
embargo = 20
initial_train = 1000 



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
from sklearn.preprocessing import StandardScaler
le = LabelEncoder()
df['regime_next_encoded'] = le.fit_transform(df['regime_next'])
print(le.classes_)
print(df['regime_next_encoded'].head())



from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, confusion_matrix

features_cols = ['returns', 'vol', 'price', 'mom_5', 'mom_21', 'drawdown']

train_idx, test_idx = splits[0]

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


print(x_train.describe())


print("Fold 1 accuracy:", accuracy_score(y_test, y_pred))
print("Confusion matrix:")
print(confusion_matrix(y_test, y_pred))


#Recall(actual change) and precision(predicted change)
actual_changed = ~df.iloc[test_idx]['same_regime']

today_regime_encoded = le.transform(df.iloc[test_idx]['regime'])
predicted_changed = (y_pred != today_regime_encoded)

from sklearn.metrics import precision_score, recall_score
print("Recall (caught transitions):", recall_score(actual_changed, predicted_changed))
print("Precision (predicted transitions that were real): ", precision_score(actual_changed, predicted_changed))



#5 folds ver.
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
    
    acc = accuracy_score(y_test, y_pred)

    actual_changed = ~df.iloc[test_idx]['same_regime']
    today_regime_encoded = le.transform(df.iloc[test_idx]['regime'])
    predicted_changed = (y_pred != today_regime_encoded)

    rec = recall_score(actual_changed, predicted_changed)
    prec = precision_score(actual_changed, predicted_changed)

    results.append({'fold': fold_num, 'accuracy': acc, 'recall': rec, 'precision': prec})
    print(f"Fold {fold_num}: acc={acc:.3f}, recall = {rec:.3f}, precision={prec:.3f}")

results_df = pd.DataFrame(results)
print(results_df)
print(results_df[['accuracy', 'recall', 'precision']].mean())
