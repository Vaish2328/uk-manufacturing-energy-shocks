# Fuel-share weighting limitation

The initial design considered a fuel-share-weighted exposure measure:

`PreShockEnergyIntensity_s × Σ_f(FuelShare_s,f × ΔEnergyPrice_f,t)`

The relevant ONS workbook was identified and its structure was inspected. However, the exact historical 2018–2020 sector/fuel cells required for the planned weights were not safely recoverable through the public workbook interface used during the project.

No gas, electricity or other-fuel shares were guessed, back-filled or fabricated.

The final primary measure therefore uses continuous pre-shock sector energy intensity interacted with the DESNZ **All Fuels** industrial price change. Gas-only and electricity-only common price interactions are retained as robustness checks.

This is a measurement limitation and should remain explicit when interpreting the results.
