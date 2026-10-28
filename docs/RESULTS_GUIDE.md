# Results guide

The committed results are intentionally split into auditable tables rather than a single opaque output file.

## Main model

`results/tables/01_MAIN_MODELS.csv`

Contains the primary ECEI coefficient for producer-price and production outcomes with:

- Driscoll–Kraay standard error and p-value;
- 95% DK confidence interval;
- sector-clustered sensitivity;
- HC3 sensitivity;
- sample size and model fit.

## Diagnostics

`02_DIAGNOSTICS.csv` reports Breusch–Pagan, residual AR(1), Pesaran CD and the selected covariance approach.

## Dynamic sensitivity

`03_LAG_SENSITIVITY.csv` compares contemporaneous, one-quarter, two-quarter and distributed-lag specifications.

## Crisis-window sensitivity

`04_CRISIS_SENSITIVITY.csv` compares the main 2021Q1–2023Q4 crisis period with a narrower 2021Q2–2023Q2 window.

## Exposure-definition robustness

`05_EXPOSURE_DEFINITION_ROBUSTNESS.csv` compares:

- log-z pre-shock energy intensity × All Fuels;
- raw-z energy intensity × All Fuels;
- winsorised-log intensity × All Fuels;
- log-z intensity × gas-price change;
- log-z intensity × electricity-price change.

## Leave-one-sector-out robustness

`06_LEAVE_ONE_SECTOR_OUT.csv` is a key result because the final panel contains only seven sectors. It shows that the producer-price coefficient is highly sensitive to exclusion of C13 textiles.

## Descriptive evidence

`07_DESCRIPTIVE_STATISTICS.csv` and `08_SECTOR_PRE_SHOCK_INTENSITY.csv` provide the summary distributions and sector exposure evidence.

## Findings log

`09_FINDINGS_LOG.csv` translates the numerical output into deliberately bounded claims. It records both the evidence and the maximum defensible interpretation, reducing the risk of overclaiming statistical significance.
