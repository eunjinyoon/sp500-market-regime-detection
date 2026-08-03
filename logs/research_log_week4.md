## Week 4: regime risk/return characterization
**Did**
- Computed Sharpe, skew, excess kurtosis per regime
- Ran ANOVA, Kruskal-Wallis, Levene's significance tests
- Computed mean/min drawdown and % days below -10% per regime; visualized with bar charts and boxplot

**Found**
- All regimes negatively skewed — downside shocks dominate in every regime
- Calm has hidden tail risk — tightest IQR but second-highest kurtosis (1.876)
- Crisis Sharpe (0.658) beats Normal (0.460) and Elevated (0.625) despite highest volatility
- Regimes predict risk magnitude, not return direction (ANOVA p=0.85 vs Levene's p≈0)
- Drawdown orders perfectly Calm→Normal→Elevated→Crisis across all three metrics

Implication for Weeks 5–7: regime is a risk-scaling feature, not a directional signal