# Australian beer production — time series

Install Python 3.11+ and `python -m pip install -e .`. For Chronos forecasts use `python -m pip install -e ".[forecast]"`.

- `src/beer_timeseries/`: reusable helpers, including the attributed Diebold–Mariano implementation.
- `scripts/`: decomposition, diagnostics and the working forecast variant.
- `data/raw/`: original CSV inputs; `results/tables/` and `results/figures/`: retained reference results.
- `reports/`: submitted report. `archive/`: distinct historical scripts, not active entry points.

From the repository root: `python -m scripts.decomposition`, `python -m scripts.analysis`, or `python -m scripts.forecast`.
These are experiment scripts: analysis/forecast import the decomposition script, which runs decomposition and plots. They can access the online ausbeer dataset; Chronos downloads model weights. New results go to `results/generated/`, not the retained reference figures/tables.

The working and submitted forecasts differ in Chronos arguments and aggregation. The submitted version is preserved verbatim at `archive/submitted/ProjektPredykcja.py`; neither is declared scientifically superior. The early script in archive requires the unavailable course helper Lista2. See `docs/file-migration.json` for every original path and retained identical content. Versions of the original environment are unknown; dependency declarations are not a lockfile. Numerical experiments were not rerun during organization.

## Migration checks

After installation: `python -m unittest discover -s tests -v`. These small checks do not run the full research experiments.
