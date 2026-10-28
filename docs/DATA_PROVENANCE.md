# Data provenance

The project uses only public secondary data from UK official sources. The raw provider workbooks remain authoritative; this repository stores frozen project-relevant extracts so the analysis can be reproduced exactly.

## ONS Index of Production

Used for quarterly manufacturing production-volume outcomes. Monthly official series were converted to the project quarterly extract before the final modelling stage.

## ONS Producer Price Inflation

Used for manufacturing output-price indices. Only sectors with a defensible matched broad PPI series were retained in the main two-outcome panel.

## ONS energy intensity by industry

The 2018, 2019 and 2020 energy-intensity values are used to construct a fixed pre-shock exposure measure. The arithmetic mean is calculated before the major 2021–2023 energy-price shock.

## DESNZ industrial energy price indices

Quarterly gas, electricity and All Fuels price indices from QEP 3.3.1 are used to construct common industrial energy-price changes from 2019 Q1 to 2026 Q2.

## Sector concordance decision

The final sample is determined by data comparability, not by the sign or statistical significance of the results. Seven sectors have consistent coverage across production, producer-price and energy-intensity measures. C23 is not forced into the main model because the corresponding broad output-PPI mapping was not retained.

## Revision control

ONS and DESNZ series can be revised. The repository therefore contains frozen extracts used for the reported analysis. Re-running the study from newer provider workbooks may produce small differences and should be treated as a new data version rather than silently replacing the frozen evidence base.
