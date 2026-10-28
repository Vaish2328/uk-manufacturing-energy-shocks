# Data dictionary

| Variable | Definition | Role |
|---|---|---|
| `sector_code` | Project manufacturing sector code | Panel identifier |
| `sector_name` | Manufacturing sector label | Descriptor |
| `quarter` | Quarter in `YYYY Qn` format | Time identifier |
| `iop_index` | ONS Index of Production, seasonally adjusted | Production outcome level |
| `ppi_output_index` | ONS output PPI, 2015=100 | Price outcome level |
| `pre_shock_energy_intensity_mean` | Mean ONS energy intensity, 2018–2020 | Fixed sector exposure |
| `log_energy_intensity_z` | Standardised log of pre-shock mean intensity | Primary exposure scale |
| `desnz_gas_index` | DESNZ industrial gas price index, 2025=100 | Robustness price series |
| `desnz_electricity_index` | DESNZ industrial electricity price index, 2025=100 | Robustness price series |
| `desnz_all_fuels_index` | DESNZ All Fuels industrial price index, 2025=100 | Main price-shock level |
| `dln_output_pct` | 100 × quarterly log change in IoP | Main outcome |
| `dln_ppi_pct` | 100 × quarterly log change in PPI | Main outcome |
| `dln_desnz_gas_pct` | Quarterly log change in gas index | Robustness shock |
| `dln_desnz_electricity_pct` | Quarterly log change in electricity index | Robustness shock |
| `dln_desnz_all_fuels_pct` | Quarterly log change in All Fuels index | Main common shock |
| `ecei_all` | log-intensity z-score × All Fuels price change | Primary explanatory variable |
| `ecei_all_l1` | One-quarter lag of primary ECEI | Dynamic robustness |
| `ecei_all_l2` | Two-quarter lag of primary ECEI | Dynamic robustness |
| `ecei_gas` | log-intensity z-score × gas price change | Exposure robustness |
| `ecei_electricity` | log-intensity z-score × electricity price change | Exposure robustness |
| `crisis_2021_2023` | Indicator for 2021Q1–2023Q4 | State-dependence test |
| `crisis_alt_2021Q2_2023Q2` | Alternative narrower crisis indicator | Sensitivity |
| `ecei_all_x_crisis` | ECEI × main crisis indicator | State interaction |
| `ecei_all_x_crisis_alt` | ECEI × alternative crisis indicator | State interaction |
