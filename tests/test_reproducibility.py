from pathlib import Path

import pandas as pd
import pytest

from src.analysis import run_all_models
from src.build_panel import build_panel

ROOT = Path(__file__).resolve().parents[1]


def test_panel_shape_and_sample():
    panel = build_panel(ROOT)
    assert len(panel) == 210
    assert panel["sector_code"].nunique() == 7
    assert sorted(panel["sector_code"].unique()) == ["C10", "C13", "C17", "C20", "C22", "C24", "C25"]
    assert panel["quarter"].nunique() == 30


def test_first_difference_sample_size():
    panel = build_panel(ROOT)
    assert panel["dln_ppi_pct"].notna().sum() == 203
    assert panel["dln_output_pct"].notna().sum() == 203


def test_main_coefficients_reproduce_committed_results():
    panel = build_panel(ROOT)
    actual = run_all_models(panel)["01_MAIN_MODELS.csv"].set_index("outcome")
    expected = pd.read_csv(ROOT / "results" / "tables" / "01_MAIN_MODELS.csv").set_index("outcome")

    for outcome in ["dln_ppi_pct", "dln_output_pct"]:
        assert actual.loc[outcome, "coef"] == pytest.approx(expected.loc[outcome, "coef"], abs=1e-10)
        assert actual.loc[outcome, "dk_se"] == pytest.approx(expected.loc[outcome, "dk_se"], abs=1e-10)
        assert actual.loc[outcome, "dk_p"] == pytest.approx(expected.loc[outcome, "dk_p"], abs=1e-10)
