# Research Log

## Day 1 — [2026.05.27]

**Goal:** Set up Python environment, download first market data, compute returns.

**Did:**
- Installed pandas, numpy, matplotlib, yfinance into Anaconda (base) env.
- Hit the "two Pythons" problem — VS Code was running /usr/local/bin/python3 but libraries were installed in Anaconda's Python. Resolved by setting VS Code interpreter to base via Cmd+Shift+P → Python: Select Interpreter.
- Downloaded S&P 500 (^GSPC) daily data from 2015-01-01 to present. ~2864 trading days.
- Computed daily simple returns via pct_change().

**Decisions:**
- Using ^GSPC (S&P 500) as the primary index. Broad market, clean long history, appropriate for regime-level analysis.
- Start date 2015-01-01 — gives ~10 years incl. COVID stress period.

**Findings:**
- Mean daily return ≈ 0.05%, daily std ≈ 1.12%, min ≈ -12% (COVID), max ≈ +9.5%.
- Confirmed: aggregate statistics hide regime variation. The single std of 1.12% averages calm and crisis together.

**Open / Next:**
- Visualize returns; check whether volatility clustering is visible.

---

## Day 2 — [2026.05.29]

**Goal:** Visualize returns, build first regime-detection tool (rolling volatility), make initial regime labels.

**Did:**
- Plotted daily returns 2015–present. Volatility clustering clearly visible — calm periods punctuated by stress bursts, esp. March 2020.
- Computed 21-day rolling volatility, annualized via ×√252. Plotted.
- Ran diagnostic on rolling vol distribution: median ≈ 0.124, 75th ≈ 0.18, 90th ≈ 0.24, 95th ≈ 0.29, max ≈ 0.97.
- Designed four-regime labeling scheme based on rolling vol thresholds.
- Started label_regimes.py — got KeyError due to yfinance multi-level column issue; debugging deferred to tomorrow.

**Decisions:**
- 21-day rolling window: ~1 trading month, conventional, balances responsiveness and stability.
- Fixed thresholds (not percentile-based): returns are already on a scale-invariant basis, so fixed values have stable meaning across time.
- Four buckets rather than two: recovers gradation lost by binary calm/turbulent split; balances interpretability and resolution.
- Thresholds: Calm <0.13, Normal 0.13–0.18, Elevated 0.18–0.24, Crisis ≥0.24.
- Threshold values anchored to empirical distribution: 0.13 ≈ median, 0.24 ≈ 90th percentile. Not arbitrary round numbers.
- Chose "Position A" (crisis = top ~10%, broadly defined) over "Position B" (crisis = top ~3%, rare-events only): goal is to study patterns *within* stressed regimes, not just detect their existence. Inclusive coverage gives enough data points to compute meaningful regime statistics.

**Open / Next:**
- Fix the column-name bug in label_regimes.py (likely needs .squeeze() + iloc fix per yfinance multi-level output).
- Run groupby('regime')['return'].describe() — this is the first real test of the thesis: do regimes actually have statistically distinct return characteristics?
- Consider robustness check: do regime differences hold if thresholds shift by ±0.02?

**Reflections:**
- Big lesson today: every methodological choice should be tied to a research purpose. The threshold value isn't an aesthetic decision — it's downstream of "what do I want the label to capture." This framing should carry into later phases.