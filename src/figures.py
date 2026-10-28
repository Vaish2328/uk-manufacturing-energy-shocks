from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import statsmodels.api as sm

from .analysis import quarter_sort_key


def _residualize(values, data: pd.DataFrame) -> np.ndarray:
    sectors = sorted(data["sector_code"].unique())
    quarters = sorted(data["quarter"].unique(), key=quarter_sort_key)
    X = []
    for _, r in data.iterrows():
        row = [1.0]
        row += [float(r["sector_code"] == s) for s in sectors[1:]]
        row += [float(r["quarter"] == q) for q in quarters[1:]]
        X.append(row)
    return sm.OLS(np.asarray(values, dtype=float), np.asarray(X, dtype=float)).fit().resid


def make_figures(repo_root: Path, panel: pd.DataFrame, tables: dict[str, pd.DataFrame]) -> None:
    out = repo_root / "results" / "figures"
    out.mkdir(parents=True, exist_ok=True)

    prices = panel[["quarter", "desnz_gas_index", "desnz_electricity_index", "desnz_all_fuels_index"]].drop_duplicates("quarter")
    prices = prices.assign(_q=prices["quarter"].map(quarter_sort_key)).sort_values("_q")
    plt.figure(figsize=(10, 5.5))
    plt.plot(prices["quarter"], prices["desnz_gas_index"], label="Gas")
    plt.plot(prices["quarter"], prices["desnz_electricity_index"], label="Electricity")
    plt.plot(prices["quarter"], prices["desnz_all_fuels_index"], label="All fuels")
    plt.xticks(rotation=60, ha="right")
    plt.ylabel("Index (2025=100)")
    plt.title("DESNZ Industrial Fuel Price Indices, 2019 Q1–2026 Q2")
    plt.legend()
    plt.tight_layout()
    plt.savefig(out / "Figure_1_DESNZ_industrial_energy_prices.png", dpi=200)
    plt.close()

    intensity = panel[["sector_code", "pre_shock_energy_intensity_mean"]].drop_duplicates().sort_values("pre_shock_energy_intensity_mean")
    plt.figure(figsize=(9, 5.5))
    plt.bar(intensity["sector_code"], intensity["pre_shock_energy_intensity_mean"])
    plt.ylabel("TJ per £m")
    plt.title("Pre-shock Energy Intensity: 2018–2020 Mean")
    plt.tight_layout()
    plt.savefig(out / "Figure_2_pre_shock_energy_intensity.png", dpi=200)
    plt.close()

    for outcome, label, filename in [
        ("dln_ppi_pct", "Producer-price change", "Figure_3_partial_ECEI_vs_PPI.png"),
        ("dln_output_pct", "Production change", "Figure_4_partial_ECEI_vs_output.png"),
    ]:
        data = panel.dropna(subset=["ecei_all", outcome]).copy()
        xr = _residualize(data["ecei_all"], data)
        yr = _residualize(data[outcome], data)
        slope, intercept = np.polyfit(xr, yr, 1)
        xx = np.linspace(xr.min(), xr.max(), 100)
        plt.figure(figsize=(8, 5.5))
        plt.scatter(xr, yr, alpha=0.65)
        plt.plot(xx, slope * xx + intercept)
        plt.xlabel("ECEI residual after sector and quarter fixed effects")
        plt.ylabel(f"{label} residual")
        plt.title(f"Fixed-effects Partial Relationship: ECEI and {label}")
        plt.tight_layout()
        plt.savefig(out / filename, dpi=200)
        plt.close()

    main = tables["01_MAIN_MODELS.csv"]
    rows = [main.loc[main["outcome"] == x].iloc[0] for x in ["dln_ppi_pct", "dln_output_pct"]]
    coef = [float(r.coef) for r in rows]
    low = [float(r.dk_ci_low) for r in rows]
    high = [float(r.dk_ci_high) for r in rows]
    y = np.arange(2)
    xerr = np.asarray([
        [coef[i] - low[i] for i in range(2)],
        [high[i] - coef[i] for i in range(2)],
    ])
    plt.figure(figsize=(8, 4.8))
    plt.errorbar(coef, y, xerr=xerr, fmt="o", capsize=5)
    plt.axvline(0, linewidth=1)
    plt.yticks(y, ["Producer prices", "Production"])
    plt.xlabel("ECEI coefficient with 95% Driscoll–Kraay CI")
    plt.title("Main Fixed-Effects Estimates")
    plt.tight_layout()
    plt.savefig(out / "Figure_5_main_coefficients_DK.png", dpi=200)
    plt.close()

    loo = tables["06_LEAVE_ONE_SECTOR_OUT.csv"]
    loo = loo.loc[loo["outcome"] == "dln_ppi_pct"].copy()
    coef = loo["coef"].astype(float).tolist()
    low = loo["dk_ci_low"].astype(float).tolist()
    high = loo["dk_ci_high"].astype(float).tolist()
    y = np.arange(len(loo))
    xerr = np.asarray([
        [coef[i] - low[i] for i in range(len(coef))],
        [high[i] - coef[i] for i in range(len(coef))],
    ])
    plt.figure(figsize=(9, 5.5))
    plt.errorbar(coef, y, xerr=xerr, fmt="o", capsize=4)
    plt.axvline(0, linewidth=1)
    plt.yticks(y, [f"Exclude {s}" for s in loo["excluded_sector"]])
    plt.xlabel("PPI ECEI coefficient, 95% DK CI")
    plt.title("Leave-One-Sector-Out Robustness: Producer Prices")
    plt.tight_layout()
    plt.savefig(out / "Figure_6_leave_one_sector_out_PPI.png", dpi=200)
    plt.close()
