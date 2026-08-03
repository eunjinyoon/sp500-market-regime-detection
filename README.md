# S&P 500 Market Regime Detection & Regime-Aware Return Prediction

**An independent research project investigating whether market regimes have statistically distinct risk/return profiles, and whether regime-aware features improve return prediction.**

---

## Motivation

Markets don't behave the same way in calm periods as they do in crises — volatility clusters, correlations shift, and factor exposures change. This project asks two concrete questions:

1. Do S&P 500 market regimes (defined by realized volatility) have **statistically distinct** risk/return characteristics?
2. Can **regime-aware features** meaningfully improve short-horizon return and regime-transition prediction, beyond a naive persistence baseline?

The project builds an end-to-end pipeline: **regime labeling → econometric analysis → predictive modeling with walk-forward validation → portfolio construction**.

---

## Key Findings So Far

- **The regime framework is a volatility tool, not a direction predictor.** Levene's test confirms highly significant variance differences across regimes (p ≈ 0), while ANOVA (p = 0.85) shows regimes do *not* predict mean return direction. Regimes cluster volatility, not returns.
- **Crisis is stickier than intuition suggests.** Transition matrix analysis shows Calm → Crisis and Crisis → Calm transitions are effectively zero. Elevated and Normal regimes act as buffer states — the market has to pass through them.
- **Crisis carries a statistically significant forward-return premium.** A t-test confirms a significant 21-day forward return premium for Crisis over Elevated regimes — consistent with a risk-compensation story, not just noise.
- **Factor exposure is regime-dependent, but beta isn't.** CAPM vs. Fama-French three-factor regressions (case study: Goldman Sachs) show beta is stable across regimes, but R² rises monotonically into Crisis (0.277 → 0.680 unconditional CAPM → FF). HML is consistently significant — GS behaves as a value stock — while SMB is negligible and alpha stays insignificant throughout.
- **A 93.9% naive accuracy baseline makes vanilla accuracy a poor metric.** Regime persistence means a "predict no change" baseline is already ~94% accurate. Walk-forward logistic regression scored ~79.5% accuracy but only ~46.8% recall and ~24.4% precision on regime transitions — the metric that actually matters.
- **Random forest trades recall for precision — the wrong tradeoff for this use case.** A class-weight-balanced random forest improved precision to ~53.7% (vs. 24.4%) but recall fell to ~29.5% (vs. 46.8%). Feature importances confirm volatility dominates the signal (~59%), consistent with the ANOVA/Levene's results above. Because the downstream allocation rule is continuous (not a hard on/off switch), missed transitions are costlier than false alarms — so logistic regression's higher-recall profile was used for the deployable portfolio strategy.
- **A regime-aware, volatility-targeting strategy improves risk-adjusted returns — even with a realistic, imperfect model.** Using true regime labels (perfect-information benchmark), the strategy cut max drawdown from -33.9% to -12.1% and raised Sharpe from 0.828 to 0.961 versus buy-and-hold, at the cost of some raw return. Re-run using actual walk-forward (logistic regression) predictions on out-of-sample test folds, the strategy still outperformed buy-and-hold on a risk-adjusted basis (Sharpe 0.458 vs. 0.410, comparable drawdown reduction) — confirming the effect holds up under realistic, non-hindsight conditions, not just the idealized case.

---

## Methodology

### 1. Regime Labeling
- S&P 500 daily data via `yfinance`
- Regimes defined using **fixed volatility thresholds**, chosen (over percentile-based cuts) to guarantee enough observations in the Crisis bucket for reliable within-regime analysis:

  | Regime | Realized Volatility |
  |---|---|
  | Calm | < 0.13 |
  | Normal | 0.13 – 0.18 |
  | Elevated | 0.18 – 0.24 |
  | Crisis | ≥ 0.24 |

- Feature engineering: momentum and drawdown features

### 2. Econometric Analysis
- Episode duration analysis and regime transition matrices
- Statistical testing: **ANOVA, Levene's test, Kruskal-Wallis** for within/across-regime return and variance differences
- Forward return feature construction (21-day horizon)
- Risk/return profiling: Sharpe ratios, skewness, kurtosis, drawdown metrics by regime
- **CAPM and Fama-French three-factor regressions** across regimes (Fama-French data via `pandas_datareader`), case study on Goldman Sachs

### 3. Predictive Modeling — Walk-Forward Validation
- Target: `regime_next`, constructed via `.shift(-1)`
- Naive persistence baseline: ~93.9% accuracy (~6% daily transition rate)
- Custom `walk_forward_splits()`: expanding window, **20-day embargo** to prevent look-ahead bias at fold boundaries, 5 folds
- **Logistic regression**: accuracy ~79.5%, recall ~46.8%, precision ~24.4%
- **Random forest** (class-weight balanced): accuracy ~87.7%, recall ~29.5%, precision ~53.7% — better precision, worse recall; feature importances show volatility dominates (~59%), consistent with the Levene's/ANOVA results
- Model selection for downstream use was driven by the cost structure of the allocation rule (see below), not by accuracy alone

### 4. Risk & Portfolio Analysis
- **Allocation rule**: volatility targeting — `weight_equity_t = target_volatility / realized_vol_t` (capped at 1.0, no leverage), with `target_volatility` anchored to the Calm regime's average realized volatility. Chosen because Levene's test shows regimes differ in variance, not mean return (ANOVA), so a variance-based rule is the one actually supported by the data
- `.shift(1)` applied to prevent using same-day volatility (which includes same-day returns) to set same-day exposure — a look-ahead check analogous to the walk-forward embargo
- **Benchmark A (perfect information)** — allocation driven by true regime labels:

  | | Return | Max Drawdown | Sharpe |
  | Buy-and-hold | higher | -33.9% | 0.828 |
  | Regime-aware strategy | lower | **-12.1%** | **0.961** |

- **Benchmark B (realistic)** — allocation driven by out-of-sample walk-forward (logistic regression) predictions, evaluated on the same test-fold dates:

  | | Max Drawdown | Sharpe |
  | Buy-and-hold (same dates) | -30.6% | 0.410 |
  | Regime-aware strategy (predicted) | **-12.2%** | **0.458** |

- **Takeaway**: model imperfection costs some Sharpe relative to the perfect-information case (0.961 → 0.458, on a shorter/different date range), but the strategy still beats buy-and-hold on a risk-adjusted basis even with a realistic, noisy prediction model — the core result is not just a hindsight artifact

---

## Final Synthesis

Returning to the two questions posed at the outset:

**1. Do S&P 500 market regimes have statistically distinct risk/return characteristics?**
Yes, but asymmetrically. Regimes differ sharply in **variance** (Levene's test, p ≈ 0) but not in **mean return direction** (ANOVA, p = 0.85). The transition matrix reinforces this as a genuine structural feature rather than noise: Crisis is a sticky, hard-to-exit state, and the market must pass through Elevated/Normal as buffer states rather than jumping directly between calm and crisis conditions. The one departure from "no return signal" is the Crisis-over-Elevated forward-return premium, which is consistent with a risk-compensation story rather than contradicting the volatility-clustering framework.

**2. Can regime-aware features improve prediction and, ultimately, real decisions?**
Partially, and the honest answer required stacking three separate checks rather than trusting any one metric in isolation:
- **Prediction alone was weak.** Against a 93.9% naive persistence baseline, no model achieved good precision *and* recall simultaneously — logistic regression favored recall (46.8%) at the cost of precision (24.4%); random forest inverted that tradeoff (29.5% / 53.7%). Neither is a strong classifier in absolute terms.
- **But the choice of model still mattered downstream.** Because the allocation rule is continuous rather than a binary switch, missed transitions (low recall) are more costly than false alarms (low precision) — so the weaker-looking model by raw accuracy was the better choice for the actual decision being made. This is the kind of judgment that a single accuracy number would have gotten wrong.
- **And the weak model was still useful in practice.** Despite modest precision/recall, feeding real out-of-sample predictions into the volatility-targeting allocation rule (Benchmark B) preserved almost all of the risk reduction seen under perfect information (Benchmark A) — max drawdown fell to roughly the same degree (-12.2% vs. -12.1%) — and still beat buy-and-hold on Sharpe (0.458 vs. 0.410), even though the underlying classifier was far from accurate.

**Overall conclusion**: Regime information is real and exploitable, but its value shows up more reliably in **risk management** (drawdown control, volatility targeting) than in **return prediction**. A weak classifier, paired with an allocation rule that matched the classifier's actual error profile and the regime framework's actual statistical properties (variance-based, not direction-based), was enough to produce a genuine risk-adjusted improvement over a passive benchmark — without requiring a highly accurate prediction model. That distinction — between "the model has to be right" and "the model has to be wrong in a tolerable way" — was the central practical insight of the project.

**Limitations and next steps**: results are based on a single asset (S&P 500 index) and one factor case study (Goldman Sachs); the walk-forward evaluation covers five folds (~750 test days), a moderate but not large out-of-sample sample; and the allocation rule, while motivated by the statistical findings, is one reasonable design choice among several (e.g., a discrete regime-based weighting table was considered but not implemented). Extending the prediction horizon from t+1 to t+5, and testing the allocation rule across a broader universe of assets, are natural next steps.



`Python` · `pandas` · `numpy` · `scikit-learn` · `scipy` · `matplotlib` · `yfinance` · `pandas_datareader`

---

## Repository Structure

```
├── Week1/                          # data pipeline, regime labeling
├── Week2/                          # feature engineering (momentum, drawdown)
├── Week3/                          # episode/transition analysis
├── Week4/                          # statistical testing (ANOVA, Levene's, Kruskal-Wallis)
├── Week5/                          # CAPM / Fama-French factor regressions
├── Week6/                          # walk-forward validation, logistic regression, random forest
├── summary/                        # portfolio & risk analysis, final synthesis
├── logs/                           # research log entries
├── sp500_features.csv              # engineered features dataset
├── S&P 500 Price with Marked Regimes.png
├── S&P 500 volatility.png
├── regime_boxplot.png
└── drawdown_by_regime.png
```

*Note: folders are organized by working week internally, but the README above is written thematically rather than by week, since that's the more standard framing for external readers.*

---

## Roadmap

- [x] Data pipeline, regime labeling, feature engineering
- [x] Episode/transition analysis, statistical testing
- [x] CAPM / Fama-French factor regressions
- [x] Walk-forward validation framework, logistic regression + random forest comparison
- [x] Portfolio construction, regime-aware risk analysis (perfect-information and realistic prediction-based benchmarks)
- [x] Final synthesis, writeup polish
- [ ] Extend prediction horizon (t+1 → t+5)

---

## Author

**Yoon Eunjin** — Economics, National University of Singapore
[LinkedIn](https://www.linkedin.com/in/eunjin-yoon-10b17a292/) · eunjinyoon.ej@gmail.com · GitHub repo coming soon

*This is an independent research project undertaken to explore quantitative finance methodology, from regime detection through predictive modeling and portfolio construction.*
