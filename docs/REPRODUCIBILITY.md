# Reproducibility guide

## Environment

Python 3.12 or later is recommended.

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

## Full rebuild

From the repository root:

```bash
python -m src.pipeline
```

The pipeline performs three stages:

1. rebuilds `data/processed/panel_continuous_ecei_2019Q1_2026Q2.csv` from the verified raw extracts;
2. re-estimates all main and robustness tables in `results/tables/`;
3. regenerates all figures in `results/figures/`.

## Validation

```bash
pytest -q
```

Expected result:

```text
3 passed
```

The coefficient tests use strict numerical tolerances. If a future dependency version materially changes the econometric covariance implementation, investigate the difference before updating the expected outputs.

## Makefile shortcuts

```bash
make install
make all
make test
```

## Revisions

Do not overwrite the frozen raw extracts with newly released ONS/DESNZ data and still describe the output as the same replication. If provider data are updated, create a new version/tag and record the download date and changed observations.
