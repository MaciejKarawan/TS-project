# Australian Beer Production — Time Series Analysis

Academic project analysing quarterly Australian beer production through decomposition, diagnostics and forecasting.

## Contents

- `ProjektDekompozycja.py`: decomposition and trend modelling.
- `ProjektAnaliza.py`: statistical analysis and diagnostics.
- `ProjektPredykcja.py`: forecasting and comparison with saved predictions.
- `data/`, CSV files and `Wykresy/`: input data and saved results.
- `Projekt-return/`: retained submitted/report variant, including its original code and PDF report.
- `Projekt.py`: pre-existing file retained from this repository.

The original structure and alternative versions are preserved. Scripts expect particular working directories and may open plots, write files or fetch the `ausbeer` dataset. Dependencies include NumPy, pandas, SciPy, matplotlib, seaborn, statsmodels, Plotly and pyreadr. Local helper modules are included where found in the adjacent course directory.

The original `Projekt.py` also imports a course module named `Lista2`, which is not part of the supplied project folder. The `dm_test.py` helper is included with its original author attribution preserved. Python syntax was checked during import; full execution and reproducibility have not been validated. No licence was added or changed.
