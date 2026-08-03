import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("sp500_features.csv")

groups = df.groupby('regime')['drawdown'].agg(['mean', 'min'])
groups['pct_deep_drawdown'] = df.groupby('regime')['drawdown'].apply(lambda x: (x < -0.1).mean())

fig, axes = plt.subplots(1, 3, figsize=(15,5))

regime_order = ['Calm', 'Normal', 'Elevated', 'Crisis']

axes[0].bar(regime_order, groups.loc[regime_order, 'mean'])
axes[0].set_title('Mean Drawdown by Regime')
axes[0].set_ylabel('Drawdown')

axes[1].bar(regime_order, groups.loc[regime_order, 'min'])
axes[1].set_title('Min Drawdown by Regime')

axes[2].bar(regime_order, groups.loc[regime_order, 'pct_deep_drawdown'])
axes[2].set_title('% Days with Drawdown <-10%')
axes[2].set_ylabel('Fraction of Days')

plt.tight_layout()
plt.savefig('drawdown_by_regime.png')
plt.show()
