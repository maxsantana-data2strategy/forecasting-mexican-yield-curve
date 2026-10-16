# Forecasting the Mexican Yield Curve

Concise data-science project: analysis and forecasting of Mexico’s nominal yield curve (Oct 2006 – Sep 2026).

Quick summary

- Goal: find a low-dimensional representation of the curve (PCA) and evaluate forecasting strategies.
- Models: Persistence, direct VAR(1) on monthly changes, PCA (3 PCs) + VAR(1) on factor scores.
- Evaluation: expanding-window forecasts starting Oct 2022; horizons = 3 and 12 months; metrics = average RMSE and MAE across maturities.

Repository contents

- `notebooks/analisis_curva_banxico.ipynb` — main notebook (add locally if not present)
- `data/raw/banxico_auction_rates_monthly.csv` — raw input data (required to run scripts)
- `_run_ffill_comparison.py`, `_generate_brief_pdf.py`, `_refresh_main_notebook_outputs.py`, `_restore_levels_changes_explanation.py`, `_extract_pdf.py`, `_extract_text_pdf.py`
- `docs/` — brief PDF, reference files and figures
- `outputs/figures/` — charts used by the brief

How to run (minimal)

1. Clone the repo
2. Create a venv and install: pandas, numpy, scikit-learn, statsmodels, matplotlib, pymupdf, pillow
3. Place raw CSV at `data/raw/banxico_auction_rates_monthly.csv`
4. Run: `python _run_ffill_comparison.py`

Notes

- Visual assets referenced in README were removed per request. The docs/ and outputs/ folders still contain the original figures and briefs — add missing binary files (notebook, raw CSV) if needed.

License & tags

MIT
Topics: data-science, time-series, forecasting, PCA, economics
