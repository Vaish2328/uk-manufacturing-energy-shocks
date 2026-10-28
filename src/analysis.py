from __future__ import annotations

import math
from pathlib import Path

import numpy as np
import pandas as pd
import statsmodels.api as sm
from scipy import stats
from statsmodels.stats.diagnostic import het_breuschpagan


def quarter_sort_key(q: str) -> tuple[int, int]:
    year, qtr = q.split()
    return int(year), int(qtr[1:])


def build_design(data: pd.DataFrame, terms: list[str], outcome: str):
    cols_needed = [outcome, *terms, "sector_code", "quarter"]
    usable = data.dropna(subset=cols_needed).copy()
    sectors = sorted(usable["sector_code"].unique())
    quarters = sorted(usable["quarter"].unique(), key=quarter_sort_key)

    columns = ["const", *terms]
    columns += [f"sector_{s}" for s in sectors[1:]]
    columns += [f"quarter_{q.replace(' ', '_')}" for q in quarters[1:]]

    rows = []
    for _, r in usable.iterrows():
        x = [1.0, *[float(r[t]) for t in terms]]
        x += [float(r["sector_code"] == s) for s in sectors[1:]]
        x += [float(r["quarter"] == q) for q in quarters[1:]]
        rows.append(x)

    X = np.asarray(rows, dtype=float)
    y = usable[outcome].to_numpy(dtype=float)
    time_idx = usable["quarter"].map({q: i for i, q in enumerate(quarters)}).to_numpy(dtype=int)
    group_idx = usable["sector_code"].map({s: i for i, s in enumerate(sectors)}).to_numpy(dtype=int)
    return usable, y, X, columns, time_idx, group_idx, sectors, quarters


def pesaran_cd(residuals: np.ndarray, data: pd.DataFrame):
    tmp = data[["sector_code", "quarter"]].copy()
    tmp["resid"] = residuals
    pivot = tmp.pivot(index="quarter", columns="sector_code", values="resid")
    pivot = pivot.loc[sorted(pivot.index, key=quarter_sort_key)].dropna(axis=0, how="any")
    corr = pivot.corr().to_numpy()
    n = corr.shape[0]
    t = pivot.shape[0]
    upper = corr[np.triu_indices(n, 1)]
    cd = math.sqrt(2.0 * t / (n * (n - 1))) * float(upper.sum())
    p = 2.0 * (1.0 - stats.norm.cdf(abs(cd)))
    return cd, p, float(upper.mean()), n, t


def residual_ar1(residuals: np.ndarray, data: pd.DataFrame):
    tmp = data[["sector_code", "quarter"]].copy()
    tmp["resid"] = residuals
    records = []
    for sector, group in tmp.groupby("sector_code"):
        group = group.copy()
        group["_q"] = group["quarter"].map(quarter_sort_key)
        group = group.sort_values("_q")
        group["lag_resid"] = group["resid"].shift(1)
        records.append(group.dropna(subset=["lag_resid"]))
    df = pd.concat(records, ignore_index=True)
    sectors = sorted(df["sector_code"].unique())
    X = np.column_stack([
        np.ones(len(df)),
        df["lag_resid"].to_numpy(dtype=float),
        *[(df["sector_code"] == s).to_numpy(dtype=float) for s in sectors[1:]],
    ])
    fit = sm.OLS(df["resid"].to_numpy(dtype=float), X).fit(cov_type="HC3")
    return float(fit.params[1]), float(fit.bse[1]), float(fit.pvalues[1]), len(df)


def fit_model(data: pd.DataFrame, outcome: str, terms: list[str], maxlags: int = 2):
    usable, y, X, columns, time_idx, group_idx, sectors, quarters = build_design(data, terms, outcome)
    base = sm.OLS(y, X).fit()
    dk = base.get_robustcov_results(
        cov_type="hac-groupsum", time=time_idx, maxlags=maxlags, use_correction="cluster"
    )
    cluster = base.get_robustcov_results(
        cov_type="cluster", groups=group_idx, use_correction=True
    )
    hc3 = base.get_robustcov_results(cov_type="HC3")

    results = []
    for term in terms:
        i = columns.index(term)
        ci = dk.conf_int()[i]
        results.append({
            "outcome": outcome,
            "term": term,
            "coef": float(base.params[i]),
            "dk_se": float(dk.bse[i]),
            "dk_p": float(dk.pvalues[i]),
            "dk_ci_low": float(ci[0]),
            "dk_ci_high": float(ci[1]),
            "cluster_se": float(cluster.bse[i]),
            "cluster_p": float(cluster.pvalues[i]),
            "hc3_se": float(hc3.bse[i]),
            "hc3_p": float(hc3.pvalues[i]),
            "n": int(base.nobs),
            "r2": float(base.rsquared),
            "adj_r2": float(base.rsquared_adj),
        })

    bp = het_breuschpagan(base.resid, X)
    rho, rho_se, rho_p, _ = residual_ar1(base.resid, usable)
    cd, cd_p, avg_corr, n_sec, t_common = pesaran_cd(base.resid, usable)
    diagnostics = {
        "outcome": outcome,
        "terms": "+".join(terms),
        "n": int(base.nobs),
        "N_sectors": n_sec,
        "T_common": t_common,
        "BP_LM": float(bp[0]),
        "BP_LM_p": float(bp[1]),
        "BP_F": float(bp[2]),
        "BP_F_p": float(bp[3]),
        "resid_AR1": rho,
        "resid_AR1_se": rho_se,
        "resid_AR1_p": rho_p,
        "Pesaran_CD": cd,
        "Pesaran_CD_p": cd_p,
        "avg_pairwise_resid_corr": avg_corr,
        "selected_covariance": "Driscoll-Kraay / hac-groupsum, maxlags=2",
    }
    return results, diagnostics


def run_all_models(panel: pd.DataFrame) -> dict[str, pd.DataFrame]:
    outputs: dict[str, pd.DataFrame] = {}

    main_rows = []
    diagnostic_rows = []
    for outcome in ["dln_ppi_pct", "dln_output_pct"]:
        r, d = fit_model(panel, outcome, ["ecei_all"])
        main_rows.extend(r)
        diagnostic_rows.append(d)
    outputs["01_MAIN_MODELS.csv"] = pd.DataFrame(main_rows)
    outputs["02_DIAGNOSTICS.csv"] = pd.DataFrame(diagnostic_rows)

    lag_rows = []
    lag_specs = [
        ("current", ["ecei_all"]),
        ("lag1", ["ecei_all_l1"]),
        ("lag2", ["ecei_all_l2"]),
        ("current_plus_lag1", ["ecei_all", "ecei_all_l1"]),
        ("current_plus_lag1_plus_lag2", ["ecei_all", "ecei_all_l1", "ecei_all_l2"]),
    ]
    for outcome in ["dln_ppi_pct", "dln_output_pct"]:
        for spec, terms in lag_specs:
            r, _ = fit_model(panel, outcome, terms)
            for row in r:
                row["specification"] = spec
                lag_rows.append(row)
    outputs["03_LAG_SENSITIVITY.csv"] = pd.DataFrame(lag_rows)

    crisis_rows = []
    for outcome in ["dln_ppi_pct", "dln_output_pct"]:
        for label, interaction in [
            ("2021Q1_2023Q4", "ecei_all_x_crisis"),
            ("2021Q2_2023Q2", "ecei_all_x_crisis_alt"),
        ]:
            r, _ = fit_model(panel, outcome, ["ecei_all", interaction])
            for row in r:
                row["crisis_window"] = label
                crisis_rows.append(row)
    outputs["04_CRISIS_SENSITIVITY.csv"] = pd.DataFrame(crisis_rows)

    exposure_rows = []
    for outcome in ["dln_ppi_pct", "dln_output_pct"]:
        for term, label in [
            ("ecei_all", "log_intensity_x_all_fuels"),
            ("ecei_all_rawz", "raw_intensity_z_x_all_fuels"),
            ("ecei_all_wins", "winsorised_log_intensity_x_all_fuels"),
            ("ecei_gas", "log_intensity_x_gas_price"),
            ("ecei_electricity", "log_intensity_x_electricity_price"),
        ]:
            r, _ = fit_model(panel, outcome, [term])
            row = r[0]
            row["exposure_definition"] = label
            exposure_rows.append(row)
    outputs["05_EXPOSURE_DEFINITION_ROBUSTNESS.csv"] = pd.DataFrame(exposure_rows)

    loo_rows = []
    sectors = sorted(panel["sector_code"].unique())
    sector_names = panel.drop_duplicates("sector_code").set_index("sector_code")["sector_name"].to_dict()
    for outcome in ["dln_ppi_pct", "dln_output_pct"]:
        for excluded in sectors:
            subset = panel.loc[panel["sector_code"] != excluded].copy()
            r, _ = fit_model(subset, outcome, ["ecei_all"])
            row = r[0]
            row["excluded_sector"] = excluded
            row["excluded_sector_name"] = sector_names[excluded]
            loo_rows.append(row)
    outputs["06_LEAVE_ONE_SECTOR_OUT.csv"] = pd.DataFrame(loo_rows)

    desc_rows = []
    for variable in ["dln_ppi_pct", "dln_output_pct", "dln_desnz_all_fuels_pct", "ecei_all"]:
        s = panel[variable].dropna().astype(float)
        desc_rows.append({
            "variable": variable,
            "n": int(s.size),
            "mean": float(s.mean()),
            "sd": float(s.std(ddof=1)),
            "min": float(s.min()),
            "p25": float(s.quantile(0.25)),
            "median": float(s.median()),
            "p75": float(s.quantile(0.75)),
            "max": float(s.max()),
        })
    outputs["07_DESCRIPTIVE_STATISTICS.csv"] = pd.DataFrame(desc_rows)

    intensity = panel[[
        "sector_code", "sector_name", "pre_shock_energy_intensity_mean", "log_energy_intensity_z"
    ]].drop_duplicates("sector_code").sort_values("sector_code")
    raw_intensity = pd.read_csv(Path(__file__).resolve().parents[1] / "data" / "raw" / "ons_energy_intensity_2018_2020.csv")
    intensity = intensity.merge(raw_intensity[["sector_code", "2018_TJ_per_GBPm", "2019_TJ_per_GBPm", "2020_TJ_per_GBPm"]], on="sector_code")
    intensity = intensity.rename(columns={
        "2018_TJ_per_GBPm": "2018", "2019_TJ_per_GBPm": "2019", "2020_TJ_per_GBPm": "2020",
        "pre_shock_energy_intensity_mean": "mean_2018_2020",
    })
    intensity["note"] = ""
    intensity.loc[intensity["sector_code"] == "C13", "note"] = (
        "C13 is an extreme pre-shock intensity observation and is explicitly tested in leave-one-sector-out robustness."
    )
    outputs["08_SECTOR_PRE_SHOCK_INTENSITY.csv"] = intensity[[
        "sector_code", "sector_name", "2018", "2019", "2020", "mean_2018_2020", "log_energy_intensity_z", "note"
    ]]

    main = outputs["01_MAIN_MODELS.csv"]
    loo = outputs["06_LEAVE_ONE_SECTOR_OUT.csv"]
    ppi = main.loc[main["outcome"] == "dln_ppi_pct"].iloc[0]
    out = main.loc[main["outcome"] == "dln_output_pct"].iloc[0]
    c13 = loo.loc[(loo["outcome"] == "dln_ppi_pct") & (loo["excluded_sector"] == "C13")].iloc[0]
    findings = [
        {
            "finding_id": "F1",
            "research_question": "RQ1/RQ2 – producer-price adjustment",
            "result": f"Primary two-way FE estimate for ECEI: beta={ppi.coef:.4f}, DK SE={ppi.dk_se:.4f}, p={ppi.dk_p:.4f}.",
            "interpretation": "In the full seven-sector panel, higher continuous pre-shock energy intensity is associated with a lower relative quarterly producer-price response to a common all-fuels price shock, conditional on sector and quarter fixed effects.",
            "robustness": f"Not stable to sector composition: excluding C13 changes the coefficient to {c13.coef:.4f} (DK p={c13.dk_p:.4f}).",
            "claim_strength": "Fragile association; do not claim a robust negative pass-through effect or causality.",
        },
        {
            "finding_id": "F2",
            "research_question": "RQ1/RQ2 – production adjustment",
            "result": f"Primary output estimate: gamma={out.coef:.4f}, DK SE={out.dk_se:.4f}, p={out.dk_p:.4f}.",
            "interpretation": "The main specification does not show statistically robust evidence that more energy-intensive sectors systematically contracted output more when the common all-fuels price index increased.",
            "robustness": "Contemporaneous and lagged output specifications remain statistically weak under DK inference.",
            "claim_strength": "No robust sector-level output effect detected in this panel.",
        },
        {
            "finding_id": "F3",
            "research_question": "RQ3 – crisis-state difference",
            "result": "ECEI × crisis interaction is not statistically significant in either crisis-window definition for either outcome under DK inference.",
            "interpretation": "The small sector panel does not provide robust evidence that the exposure-response slope changed during the defined energy-crisis window.",
            "robustness": "Two crisis windows tested.",
            "claim_strength": "Failure to detect a differential crisis slope is not proof of no crisis effect.",
        },
        {
            "finding_id": "F4",
            "research_question": "Inference / diagnostics",
            "result": "Output-model residuals show strong heteroskedasticity and cross-sectional dependence; PPI diagnostics are milder. Residual AR(1) diagnostics are not statistically strong.",
            "interpretation": "Driscoll-Kraay covariance is used as the primary common inference method; HC3 and sector-clustered results are retained as sensitivity checks.",
            "robustness": "DK maxlags=2, HC3, and sector-clustered covariance reported.",
            "claim_strength": "Inference choice is data-diagnostic driven.",
        },
        {
            "finding_id": "F5",
            "research_question": "Measurement robustness",
            "result": "Raw-z, log-z and winsorised-log continuous exposure definitions give similar full-sample directional results, while gas- and electricity-specific common-price interactions are weaker/marginal.",
            "interpretation": "Transformation choice is less important than sector composition; C13 is the dominant sensitivity issue.",
            "robustness": "Five exposure definitions plus leave-one-sector-out tests.",
            "claim_strength": "Measurement robustness is partial, not complete.",
        },
    ]
    outputs["09_FINDINGS_LOG.csv"] = pd.DataFrame(findings)
    return outputs


def save_results(repo_root: Path, outputs: dict[str, pd.DataFrame]) -> None:
    out = repo_root / "results" / "tables"
    out.mkdir(parents=True, exist_ok=True)
    for name, frame in outputs.items():
        frame.to_csv(out / name, index=False)
