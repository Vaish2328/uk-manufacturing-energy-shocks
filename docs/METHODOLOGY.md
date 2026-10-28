# Methodology

## Research design

The study uses a longitudinal secondary quantitative design. The analytical unit is a UK manufacturing sector observed quarterly from 2019 Q1 to 2026 Q2.

The empirical strategy asks whether sectors with different **pre-shock energy intensity** respond differently to the same national industrial energy-price movement. Pre-shock exposure is fixed using the 2018–2020 ONS energy-intensity mean, reducing the risk that the exposure measure itself reflects later adjustment to the 2021–2023 energy crisis.

## Frozen sample

The matched main sample contains:

- C10 — Manufacture of food products
- C13 — Manufacture of textiles
- C17 — Manufacture of paper and paper products
- C20 — Manufacture of chemicals and chemical products
- C22 — Manufacture of rubber and plastic products
- C24 — Manufacture of basic metals
- C25 — Fabricated metal products except machinery/equipment

C23 is retained in the source evidence but excluded from the matched two-outcome panel because a comparable broad output-PPI series was not retained.

## Variable construction

### Outcomes

Quarterly production change:

`100 × [ln(IoP_s,t) - ln(IoP_s,t-1)]`

Quarterly producer-price change:

`100 × [ln(PPI_s,t) - ln(PPI_s,t-1)]`

### Pre-shock energy exposure

The primary sector exposure is the standardised logarithm of mean 2018–2020 energy intensity:

`z(log(mean energy intensity_s,2018-2020))`

The log transformation is used because the cross-sector distribution is strongly right-skewed, particularly for C13 textiles.

### Energy-price shock

The primary common shock is the quarterly log change in the DESNZ **All Fuels** industrial price index:

`100 × [ln(AllFuels_t) - ln(AllFuels_t-1)]`

### Energy Cost Exposure Index (ECEI)

`ECEI_s,t = log_energy_intensity_z_s × dln_all_fuels_t`

Additional robustness versions use raw-z energy intensity, winsorised log intensity, gas-price changes and electricity-price changes.

## Main model

For producer prices:

`Δln(PPI_s,t) = α_s + λ_t + β ECEI_s,t + ε_s,t`

For production:

`Δln(Output_s,t) = α_s + λ_t + γ ECEI_s,t + ν_s,t`

`α_s` denotes sector fixed effects and `λ_t` quarter fixed effects.

Sector fixed effects absorb time-invariant sector characteristics. Quarter fixed effects absorb shocks common to all sectors in a quarter, including aggregate inflationary, pandemic-era and macroeconomic movements. Identification therefore comes from differential sector responses associated with pre-shock exposure.

## Dynamic and state-dependent specifications

The analysis tests:

- contemporaneous ECEI;
- one-quarter lag;
- two-quarter lag;
- current + lag 1;
- current + lag 1 + lag 2;
- ECEI × 2021Q1–2023Q4 crisis indicator;
- ECEI × 2021Q2–2023Q2 alternative crisis indicator.

## Diagnostics and covariance selection

The pipeline reports:

- Breusch–Pagan heteroskedasticity test;
- residual AR(1) diagnostic with sector controls;
- Pesaran cross-sectional dependence statistic.

The output model shows strong heteroskedasticity and cross-sectional dependence, while the PPI model has milder residual problems. Driscoll–Kraay-style `hac-groupsum` covariance with maximum lag 2 is therefore used as the common primary inference approach. HC3 and sector-clustered covariance estimates are retained as sensitivity checks.

## Robustness strategy

Robustness is assessed through:

1. lag sensitivity;
2. two crisis-window definitions;
3. raw-z, log-z and winsorised-log energy intensity;
4. gas-only and electricity-only common price shocks;
5. leave-one-sector-out estimation.

The leave-one-sector-out analysis is especially important because the sample contains only seven sectors and C13 is an extreme exposure observation.

## Interpretation boundary

The study is not a causal natural experiment. Results are described as **associations**, **differential responses** or **exposure relationships**. The analysis does not establish that firms consciously chose price pass-through instead of output adjustment, nor does it identify firm-level margins directly.
