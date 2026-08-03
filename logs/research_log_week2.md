## Day 1 [2026.06.01]

**Goal:** Make the data ready for analysis (labeling data by different buckets and visualizing them)

**Did:**
- Fixed the label_regimes.py bug and got regime statistics
- Visualized the price chart colored by the regimes
- Saved the cleaned data to CSV
- Added momentum (5-day and 21-day rolling mean returns) and drawdown (distance from rolling 252-day peak)

---

## Day 2, 3 [2026.06.08-09]

**Goal:** Visualize how returns and drawdowns correspond to regimes

**Did:**
- Visualized rolling volatility over time with threshold lines at 0.13, 0.18, 0.24 — confirmed volatility spikes align with known stress periods (e.g. COVID March 2020)
- Visualized return distributions by regime — Crisis regime shows ~4x larger standard deviation than Calm, confirming regimes have statistically distinct risk profiles
- Visualized drawdown over time with regime shading — steep drawdowns cluster in Crisis and Elevated regimes, while Calm periods stay near 0

**Key finding:** The four regimes (Calm, Normal, Elevated, Crisis) are empirically validated — they show meaningfully distinct return distributions and drawdown behavior. This justifies using regime labels as features in the predictive model in Weeks 6-7.