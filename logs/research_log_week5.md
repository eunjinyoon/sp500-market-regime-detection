## Week5: CAMP and Fama-French regressions

**Goal** prove whether the market price risk differs depending on the regime

Things to take about CAPM test
- its purpose: to measure how much return should an asset earn given how much market risk it carries
- Beta: how sensitive the asset's returns are to the market's returns
- Alpha: the return left over after accounting for market risk (positive --> outperforming / negative --> underperforming)

## Day 1
- executed CAPM test with sp500 and goldman sachs's data.
- learned beta is 1.21, which amplifies the market move by 21%.
- R-squared value is 0.277

## Day 2
**What I did**
- Ran separate OLS regressions of GS returns on S&P 500 returns for each regime
- Extracted beta, alpha, and R² into a comparison table

**Key findings**
- Beta is stable across regimes (1.13–1.28) — sensitivity to market moves does not spike in Crisis as hypothesized
- R² increases monotonically with stress: Calm (0.34) → Crisis (0.76) — market dominates GS returns during stress, crowding out firm-specific factors
- This suggests idiosyncratic (firm-specific) risk gets crowded out by systematic risk during stress — GS essentially becomes a market proxy in Crisis
- Alpha insignificant in all regimes (p > 0.4) — no excess return beyond market risk in any regime

## Day 3
**What I did**
- Fetched Fama-French daily factor data via pandas_datareader and merged with df_gs
- Ran unconditional and regime-conditioned Fama-French regressions for GS

**Key findings**
- Unconditional R² jumps from 0.277 (CAPM) to 0.680 (FF) — HML drives most of the improvement
- GS has strong, consistent positive HML exposure across all regimes (0.58–0.91) — behaves like a value stock, consistent with its large balance sheet
- SMB is negligible and insignificant in all regimes — no meaningful size exposure, as expected for a large-cap firm
- R² increases monotonically with stress: Calm (0.56) → Crisis (0.84) — same pattern as CAPM but stronger
- Alpha insignificant in all regimes — three factors fully explain GS's returns with no unexplained premium