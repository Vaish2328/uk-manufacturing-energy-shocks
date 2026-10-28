# Quality assurance and robustness audit

## Data checks

- source files are traceable to official ONS/DESNZ publications;
- sector matching is frozen before interpretation;
- the main panel has 7 sectors × 30 quarters = 210 level observations;
- first differencing leaves 203 usable observations;
- outcome and shock transformations use log differences;
- pre-shock exposure is fixed from 2018–2020;
- C13's extreme energy intensity is not deleted automatically and is addressed through explicit sensitivity analysis.

## Model checks

- sector fixed effects;
- quarter fixed effects;
- Breusch–Pagan heteroskedasticity diagnostic;
- residual AR(1) diagnostic;
- Pesaran cross-sectional-dependence diagnostic;
- Driscoll–Kraay primary covariance;
- HC3 sensitivity;
- sector-clustered sensitivity.

## Robustness checks

- 0-, 1- and 2-quarter exposure lags;
- distributed-lag specifications;
- two crisis-window definitions;
- raw intensity z-score;
- log intensity z-score;
- winsorised log intensity;
- gas-price interaction;
- electricity-price interaction;
- leave-one-sector-out estimation.

## Critical result audit

The full-sample producer-price coefficient is statistically precise under Driscoll–Kraay inference, but excluding C13 reverses its sign. The result is therefore explicitly labelled **fragile** rather than promoted as a stable pass-through effect.

The production coefficient is statistically weak under the primary inference approach. This is reported as failure to detect a robust effect, not evidence that no output response exists.

## Reproducibility checks

Automated tests verify:

1. final panel dimensions;
2. first-difference sample size;
3. reproduction of the main coefficients, DK standard errors and p-values.

GitHub Actions runs these checks on every push and pull request.
