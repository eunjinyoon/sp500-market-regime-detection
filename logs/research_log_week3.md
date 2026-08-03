## Day 1 [2026.06.10]

**Goal** analyze episode duration for regimes transition matrix. visualize the heat map

**Did**
- Analyzed episode durations
- Calm is the most persistent regime (mean 33.9 days, max 332) — a genuine stable state, not transient.
- Crisis is stickier than expected (mean 19.7 days), supporting the predictive thesis: sticky regimes mean today's regime informs tomorrow's.
- Elevated and Normal have more episodes (45 and 73) but shorter durations (9.6 and 8.1 days), consistent with transitional states — confirmed by the transition matrix.

- Calm and Crisis never occur consecutively (both 0.000), confirming Elevated and Normal as transitional phases.
- All regimes are strongly autocorrelated (diagonal 0.877–0.971), quantitatively confirming regime stickiness.
- Crisis only exits to Elevated (0.051), never directly to Calm or Normal — market stress unwinds gradually, not suddenly.

*used* transitional_matrix.png



## Day 2 [2026.06.11]
**Goal** Test whether each regime is distinct

**Did**
- conducted several tests that proved mean returns and distribution are not significantly different across the regimes. 
- However, regimes' variations are significantly different by each other, which indicates four buckets were successfully divided by its particular volatility
- Combined with the ANOVA and Kruskal-Wallis results, the full picture is clear: regimes are defined by volatility, not return direction. Variance is the differentiating characteristic across all four states.
- created box plots to prove different variance between regimes 



## Day 3 [2026.06.12]
**Did**
- Built return columns for next 5 and 21 days, analyzed the relationship between duration and return for each regime
- Showed risk premium effect by proving crisis's significantly higher 21-day return
- All regimes show a positive correlation between episode duration and 21-day forward returns, but the relationships are weak (Calm: 0.16, Crisis: 0.14, Elevated/Normal: ~0.05) — duration explains only a small fraction of return variance.
- For Crisis specifically, the positive correlation is consistent with mean reversion — longer periods of stress may compress valuations further, setting up larger eventual rebounds. However, with r ≈ 0.14, this is a weak signal, not a reliable predictor on its own.


## Week 3 Summary: Regime Structure, Statistical Validation, and Forward Returns

- **Regimes are persistent and structured** — Calm averages 33.9 days, Crisis 19.7 days. The transition matrix shows Calm and Crisis never occur consecutively, all regimes are strongly autocorrelated, and Crisis only transitions to Elevated.
- **Regimes are defined by risk magnitude, not return direction** — ANOVA and Kruskal-Wallis show mean returns don't differ significantly across regimes (p = 0.85, p = 0.37), but Levene's test shows variances differ significantly for every regime pair (all p ≈ 0). This validates the four-bucket framework.
- **Forward returns largely follow this pattern**, with one exception: Crisis shows a significant 21-day return premium over Elevated (p ≈ 0.000007), consistent with a risk premium effect.
- **Episode duration weakly correlates with forward returns** (Calm: 0.16, Crisis: 0.14) — a hint of mean reversion in Crisis, but too weak to be predictive alone.

**Takeaway:** Regimes encode risk level, not direction. This supports a thesis where regime-aware features improve risk-adjusted prediction, setting up Week 5 (CAPM/Fama-French) and Weeks 6–7 (prediction modeling using `fwd_return_5/21`).