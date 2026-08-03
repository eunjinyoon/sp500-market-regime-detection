## Week 6: Regression and prediction of next regime



## Day 1
**What I did**
- Built regime_next target column via .shift(-1); computed naive persistence baseline (93.9% accuracy) and transition rate (6.08%)
- Wrote and verified walk_forward_splits() with expanding window + embargo gap; confirmed fold boundaries align with known market events (fold 1 test window captures COVID crash, later folds catch 2022 selloff)
- Checked transitions-per-fold (range: 5–17 per fold); fold 3 (Mar–Nov 2021) notably low at 5, flagged as a caveat for future evaluation
- Fit logistic regression on fold 1: first attempt collapsed to predicting a single class (accuracy 19.3%) due to unscaled features (price in thousands vs. returns/vol as small decimals); fixed with StandardScaler (fit on train only, transform both) — accuracy improved to 86.7%
- Read the fold 1 confusion matrix: Crisis predicted well (81/85 correct, confusions only with neighboring Elevated); Normal weakest (9/16, confused mostly with Calm); zero Calm↔Crisis confusion, consistent with Week 3's transition-matrix finding

**Key findings**
- Overall accuracy (86.7%) is below the naive persistence baseline (93.9%) — a reminder that accuracy alone is the wrong metric here, since persistence baseline gets zero transitions right by construction while the model caught some
- Feature scaling is essential for logistic regression on this dataset given the price-level vs. return-scale mismatch




## Day 2: 5 folds
**What I did**
- Computed precision/recall for the "transition" class on fold 1 alone (reframing the 4-class problem as binary: did the regime change or not)
- Debugged two subtle bugs while building the 5-fold loop: scaler.fit_transform() mistakenly called on test data instead of .transform() (refitting on test leaks test-set statistics and breaks consistency with train-scaled coefficients), and model.predict() called on unscaled x_test instead of x_test_scaled
- Looped logistic regression across all 5 walk-forward folds, computing accuracy, recall, and precision on the transition class for each

**Key findings**
- Averaged across 5 folds: accuracy 79.5%, recall 46.8%, precision 24.4%
- Recall improved substantially over the fold-1-only result (0.333 → 0.468 average), with fold 3 reaching 0.615 — performance varies meaningfully by fold, not uniform
- Accuracy and recall are not aligned: fold 2 had the highest accuracy (0.960) but only middling recall (0.400) — reinforces that accuracy is a misleading metric for this problem
- Precision is consistently the weakest metric across all folds (0.105–0.400) — when the model flags a transition, it's wrong about 3 times out of 4, a stable pattern rather than a single bad fold
- fit() vs transform() rule generalized: .fit() = learn from data, .transform() = apply what was already learned; train gets both, test only ever gets .transform() — this applies per-fold independently (each fold gets its own fresh scaler fit on that fold's train data only)