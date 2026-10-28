from __future__ import annotations

import math
from pathlib import Path

import numpy as np
import pandas as pd

MAIN_SECTORS = ["C10", "C13", "C17", "C20", "C22", "C24", "C25"]


def quarter_sort_key(q: str) -> tuple[int, int]:
    year, qtr = q.split()
    return int(year), int(qtr[1:])


def zscore(values: pd.Series) -> pd.Series:
    return (values - values.mean()) / values.std(ddof=0)


def build_panel(repo_root: Path) -> pd.DataFrame:
    raw = repo_root / "data" / "raw"

    iop = pd.read_csv(raw / "ons_iop_quarterly_2019Q1_2026Q2.csv")
    ppi = pd.read_csv(raw / "ons_ppi_output_quarterly_2019Q1_2026Q2.csv")
    intensity = pd.read_csv(raw / "ons_energy_intensity_2018_2020.csv")
    prices = pd.read_csv(raw / "desnz_industrial_price_indices_2019Q1_2026Q2.csv")

    iop = iop.loc[iop["sector_code"].isin(MAIN_SECTORS), [
        "sector_code", "sector_name", "quarter", "iop_cvmsa_index"
    ]].rename(columns={"iop_cvmsa_index": "iop_index"})

    ppi = ppi.loc[ppi["sector_code"].isin(MAIN_SECTORS), [
        "sector_code", "quarter", "ppi_output_total_index_2015_100"
    ]].rename(columns={"ppi_output_total_index_2015_100": "ppi_output_index"})

    intensity = intensity.loc[intensity["sector_code"].isin(MAIN_SECTORS), [
        "sector_code", "pre_shock_mean_2018_2020"
    ]].rename(columns={"pre_shock_mean_2018_2020": "pre_shock_energy_intensity_mean"})

    panel = iop.merge(ppi, on=["sector_code", "quarter"], how="inner")
    panel = panel.merge(intensity, on="sector_code", how="left")
    panel = panel.merge(prices, on="quarter", how="left")

    sector_intensity = (
        panel[["sector_code", "pre_shock_energy_intensity_mean"]]
        .drop_duplicates("sector_code")
        .set_index("sector_code")["pre_shock_energy_intensity_mean"]
        .sort_index()
    )
    log_intensity = np.log(sector_intensity)
    log_intensity_z = zscore(log_intensity)
    raw_intensity_z = zscore(sector_intensity)

    p90 = float(np.quantile(sector_intensity.to_numpy(dtype=float), 0.90))
    winsor_log = np.log(sector_intensity.clip(upper=p90))
    winsor_log_z = zscore(winsor_log)

    panel["log_energy_intensity_z"] = panel["sector_code"].map(log_intensity_z)
    panel["raw_energy_intensity_z"] = panel["sector_code"].map(raw_intensity_z)
    panel["winsor_log_energy_intensity_z"] = panel["sector_code"].map(winsor_log_z)

    panel["_qkey"] = panel["quarter"].map(quarter_sort_key)
    panel = panel.sort_values(["sector_code", "_qkey"]).reset_index(drop=True)

    for source, target in [
        ("iop_index", "dln_output_pct"),
        ("ppi_output_index", "dln_ppi_pct"),
        ("gas_index_2025_100", "dln_desnz_gas_pct"),
        ("electricity_index_2025_100", "dln_desnz_electricity_pct"),
        ("all_fuels_index_2025_100", "dln_desnz_all_fuels_pct"),
    ]:
        panel[target] = panel.groupby("sector_code", sort=False)[source].transform(
            lambda s: 100.0 * np.log(s / s.shift(1))
        )

    panel["ecei_all"] = panel["log_energy_intensity_z"] * panel["dln_desnz_all_fuels_pct"]
    panel["ecei_all_rawz"] = panel["raw_energy_intensity_z"] * panel["dln_desnz_all_fuels_pct"]
    panel["ecei_all_wins"] = panel["winsor_log_energy_intensity_z"] * panel["dln_desnz_all_fuels_pct"]
    panel["ecei_gas"] = panel["log_energy_intensity_z"] * panel["dln_desnz_gas_pct"]
    panel["ecei_electricity"] = panel["log_energy_intensity_z"] * panel["dln_desnz_electricity_pct"]

    panel["ecei_all_l1"] = panel.groupby("sector_code", sort=False)["ecei_all"].shift(1)
    panel["ecei_all_l2"] = panel.groupby("sector_code", sort=False)["ecei_all"].shift(2)

    years = panel["quarter"].str.slice(0, 4).astype(int)
    quarters = panel["quarter"].str[-1].astype(int)
    panel["crisis_2021_2023"] = years.between(2021, 2023).astype(int)
    panel["crisis_alt_2021Q2_2023Q2"] = (
        ((years == 2021) & (quarters >= 2))
        | (years == 2022)
        | ((years == 2023) & (quarters <= 2))
    ).astype(int)
    panel["ecei_all_x_crisis"] = panel["ecei_all"] * panel["crisis_2021_2023"]
    panel["ecei_all_x_crisis_alt"] = panel["ecei_all"] * panel["crisis_alt_2021Q2_2023Q2"]

    panel = panel.rename(columns={
        "gas_index_2025_100": "desnz_gas_index",
        "electricity_index_2025_100": "desnz_electricity_index",
        "all_fuels_index_2025_100": "desnz_all_fuels_index",
    })

    keep = [
        "sector_code", "sector_name", "quarter", "iop_index", "ppi_output_index",
        "pre_shock_energy_intensity_mean", "log_energy_intensity_z",
        "desnz_gas_index", "desnz_electricity_index", "desnz_all_fuels_index",
        "dln_output_pct", "dln_ppi_pct", "dln_desnz_gas_pct",
        "dln_desnz_electricity_pct", "dln_desnz_all_fuels_pct", "ecei_all",
        "ecei_all_l1", "ecei_all_l2", "ecei_gas", "ecei_electricity",
        "crisis_2021_2023", "crisis_alt_2021Q2_2023Q2",
        "ecei_all_x_crisis", "ecei_all_x_crisis_alt",
        "ecei_all_rawz", "ecei_all_wins",
    ]
    return panel[keep].copy()


def save_panel(repo_root: Path, panel: pd.DataFrame) -> None:
    out = repo_root / "data" / "processed"
    out.mkdir(parents=True, exist_ok=True)
    panel.to_csv(out / "panel_continuous_ecei_2019Q1_2026Q2.csv", index=False)

    concordance = (
        panel[["sector_code", "sector_name", "pre_shock_energy_intensity_mean"]]
        .drop_duplicates("sector_code")
        .sort_values("sector_code")
        .rename(columns={"pre_shock_energy_intensity_mean": "pre_shock_mean_TJ_per_GBPm"})
    )
    concordance["main_sample"] = 1
    concordance["reason"] = "Matched IoP + output PPI + energy-intensity data"
    extra = pd.DataFrame([{
        "sector_code": "C23",
        "sector_name": "Manufacture of other non-metallic mineral products",
        "pre_shock_mean_TJ_per_GBPm": 13.91,
        "main_sample": 0,
        "reason": "Energy intensity and IoP available; broad output-PPI mapping not retained",
    }])
    pd.concat([concordance, extra], ignore_index=True).to_csv(
        out / "sector_concordance.csv", index=False
    )
