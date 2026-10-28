from __future__ import annotations

import argparse
from pathlib import Path

from .analysis import run_all_models, save_results
from .build_panel import build_panel, save_panel
from .figures import make_figures


def main() -> None:
    parser = argparse.ArgumentParser(description="Rebuild the complete analysis from verified source extracts.")
    parser.add_argument(
        "--root",
        type=Path,
        default=Path(__file__).resolve().parents[1],
        help="Repository root (defaults to the current project root).",
    )
    args = parser.parse_args()
    root = args.root.resolve()

    panel = build_panel(root)
    save_panel(root, panel)
    tables = run_all_models(panel)
    save_results(root, tables)
    make_figures(root, panel, tables)

    print(f"Panel rebuilt: {len(panel)} rows, {panel['sector_code'].nunique()} sectors")
    print("Results written to results/tables")
    print("Figures written to results/figures")


if __name__ == "__main__":
    main()
