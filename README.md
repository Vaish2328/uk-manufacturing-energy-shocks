# UK Manufacturing Energy-Price Shocks

**Pass Through or Cut Output? Energy-Price Shocks and Adjustment in UK Manufacturing, 2019–2026**

A reproducible Business Analytics research project examining whether UK manufacturing sectors with different pre-shock energy intensity adjusted to industrial energy-price shocks through **producer prices**, **production volumes**, or both.

<p align="center">
  <img src="results/figures/Figure_1_DESNZ_industrial_energy_prices.png" width="780" alt="DESNZ industrial energy price indices">
</p>

## Research questions

1. How did industrial energy-price shocks relate to producer-price changes and production volumes across UK manufacturing sectors between 2019 and 2026?
2. Does pre-shock sector energy intensity explain differences in producer-price pass-through and output adjustment across manufacturing sectors?
3. Did the relationship change during the 2021–2023 energy-crisis period compared with more stable periods?

## Analytical design

The project combines public secondary data from the **Office for National Statistics (ONS)** and the **Department for Energy Security and Net Zero (DESNZ)** into a quarterly sector panel.

- **Unit of analysis:** manufacturing sector × quarter
- **Period:** 2019 Q1–2026 Q2
- **Main sample:** 7 matched manufacturing sectors
- **Level observations:** 210
- **First-difference observations:** 203
- **Outcomes:** quarterly log change in ONS output PPI and ONS Index of Production
- **Exposure:** standardised log of mean 2018–2020 sector energy intensity × quarterly DESNZ All Fuels industrial-price change
- **Estimator:** sector and quarter fixed effects
- **Primary inference:** Driscoll–Kraay / `hac-groupsum`, max lag 2
- **Robustness:** alternative lags, crisis windows, exposure definitions, fuel-specific shocks and leave-one-sector-out tests

The core exposure measure is:

\[
ECEI_{s,t}=z\!\left(\log(EnergyIntensity_s^{2018-2020})\right)\times \Delta \log(EnergyPrice_t)
\]

This design uses pre-shock cross-sector exposure to study differential responses to a common national energy-price movement. It supports **conditional association**, not a causal claim.

## Main findings

| Outcome | ECEI coefficient | DK SE | p-value | Interpretation |
|---|---:|---:|---:|---|
| Producer-price change | -0.0241 | 0.0051 | 0.0032 | Precise in the full sample, but **not robust to sector composition** |
| Production change | 0.0703 | 0.0609 | 0.2918 | No statistically robust output response detected |

The main producer-price estimate is deliberately interpreted cautiously. When **C13 textiles** is removed, the coefficient changes sign and becomes approximately **+0.2273** (`p ≈ 0.0057`). This makes sector composition the most important robustness issue and rules out a strong claim of a stable negative pass-through effect.

The production model also shows heteroskedasticity and cross-sectional dependence, which is why Driscoll–Kraay inference is used as the common primary covariance estimator.

<p align="center">
  <img src="results/figures/Figure_5_main_coefficients_DK.png" width="650" alt="Main fixed-effects coefficient estimates">
</p>

<p align="center">
  <img src="results/figures/Figure_6_leave_one_sector_out_PPI.png" width="700" alt="Leave-one-sector-out producer price robustness">
</p>

## Repository structure

```text
.
├── data/
│   ├── raw/                  # verified project-relevant ONS/DESNZ extracts
│   └── processed/            # frozen concordance and final analytical panel
├── docs/                     # methodology, provenance, codebook and QA notes
├── results/
│   ├── figures/              # dissertation-ready figures
│   └── tables/               # main models, diagnostics and robustness tables
├── src/                      # reproducible Python pipeline
├── tests/                    # numerical reproducibility checks
├── .github/workflows/        # CI reproducibility check
├── requirements.txt
└── Makefile
```

## Reproduce the analysis

### 1. Create an environment

```bash
python -m venv .venv
source .venv/bin/activate      # Windows: .venv\\Scripts\\activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

### 2. Rebuild the panel, models and figures

```bash
python -m src.pipeline
```

or:

```bash
make all
```

### 3. Run the reproducibility checks

```bash
pytest -q
```

The tests verify the frozen sample dimensions and reproduce the main fixed-effects coefficients and Driscoll–Kraay inference from the verified source extracts.

## Data sources

The repository uses project-relevant extracts from official public sources. The complete source register is in [`docs/source_manifest.csv`](docs/source_manifest.csv).

- ONS Index of Production
- ONS Producer Price Inflation
- ONS UK Environmental Accounts: energy intensity by industry
- DESNZ industrial energy price indices (QEP 3.3.1)
- ONS contextual evidence on higher energy costs and UK businesses

Raw provider workbooks should remain the authoritative source. The included CSV files are frozen analytical extracts used to make the analysis reproducible.

## Measurement decision: fuel shares

A fuel-share-weighted sector exposure index was investigated, but the exact historical sector/fuel cells required for the intended weighting were not safely recoverable from the public workbook interface used during the project. No fuel shares were imputed or invented.

The primary specification therefore uses continuous pre-shock energy intensity interacted with the DESNZ **All Fuels** index. Gas- and electricity-specific price interactions are reported as robustness checks. See [`docs/FUEL_SHARE_LIMITATION.md`](docs/FUEL_SHARE_LIMITATION.md).

## Quality assurance

The repository includes:

- frozen sector concordance;
- source manifest and data provenance;
- explicit variable definitions;
- diagnostics for heteroskedasticity, residual serial correlation and cross-sectional dependence;
- three covariance approaches (Driscoll–Kraay, sector-clustered and HC3);
- lag and crisis-window sensitivity;
- alternative exposure definitions;
- leave-one-sector-out analysis;
- automated numerical tests in GitHub Actions.

See [`docs/QUALITY_ASSURANCE.md`](docs/QUALITY_ASSURANCE.md) for the complete audit trail.

## Limitations

The final panel contains only seven fully matched sectors, so inference is sensitive to individual sectors. C13 textiles has unusually high measured pre-shock energy intensity and materially affects the producer-price coefficient. The study also uses sector-level public data, so it cannot identify firm-level pricing decisions, margins or causal mechanisms directly.

These limitations are treated as part of the analytical result rather than hidden through selective specification.

## Author

**Vaishnavi Maila**  
MSc Business Analytics research project, 2026.

## Licence and attribution

The Python code in this repository is released under the MIT Licence. Third-party data remain subject to the terms of their original providers. ONS and UK government source data should be cited to the original publications; see [`DATA_LICENSE.md`](DATA_LICENSE.md).
