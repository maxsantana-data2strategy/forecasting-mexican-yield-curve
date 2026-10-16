# Forecasting the Mexican Yield Curve

A data-science project for the analysis and forecasting of Mexico’s nominal yield curve using monthly Banxico auction data from October 2006 to September 2026.

## Story

The Mexican yield curve is a core market signal that reflects expected rates, inflation, and macroeconomic conditions across maturities. This project studies how the curve behaves across nine instruments, how much of its variability can be captured in a small number of common factors, and whether those factors improve forecasting performance in a realistic out-of-sample setting.

Rather than relying on a single curve-fitting narrative, the project tests a practical forecasting workflow: build an interpretable view of the curve using PCA, compare it to a direct VAR(1) model on monthly changes, and benchmark both against persistence.

The result is a compact, explainable framework that connects higher-level macro structure to forecasting performance across short and medium horizons.

## Objectives

- Analyze the cross-maturity structure of Mexico’s nominal yield curve.
- Identify whether a low-dimensional representation captures most of the curve’s movement.
- Compare persistence, direct VAR(1), and PCA + VAR(1) forecasting strategies.
- Evaluate forecast accuracy at 3- and 12-month horizons using a temporal validation design.

## Scope

- Period: October 2006 to September 2026
- Instruments: CETES at 28, 91, 182, and 364 days; MBONOs at 3, 5, 10, 20, and 30 years
- Horizon: monthly data, evaluated at 3 and 12 months
- Approach: PCA on levels + VAR(1) on factor scores, benchmarked against persistence

## Data and preprocessing

The project begins with a long-form source file and transforms it into a monthly matrix with one maturity per column. Missing observations are handled with a causal forward-fill logic so that each value uses only the last known observation from the past. This is done to preserve temporal ordering and avoid leakage from future information.

Two treatments are compared in the analysis:

- Original workflow: trim to the valid start date, then forward-fill
- Corrected workflow: forward-fill first, then trim to the valid analysis window

The final analysis adopts the corrected treatment to avoid distortions caused by recutting before filling.

## Methodology

### 1) Curve structure

Principal Component Analysis is applied to the nine yield levels to identify the main modes of variation. The first three components summarize the dominant movements in the curve. These are interpreted as:

- Level
- Slope / steepness
- Curvature

### 2) Forecasting models

Three forecasting strategies are evaluated:

- Persistence: last observed value is used as the forecast
- Direct VAR(1): forecast monthly changes jointly for all maturities
- PCA + VAR(1): forecast the principal component scores and reconstruct the curve

### 3) Forecast validation

The evaluation respects temporal order. The training sample ends in September 2022 and the forecasting origins begin in October 2022. Forecast errors are assessed using average RMSE and MAE across maturities.

## Key findings

- Three common factors explain approximately 99.38% of the total variance.
- The first principal component alone explains roughly 94.09% of the movement in the curve.
- At the 3-month horizon, the direct VAR(1) model performs best in the selected design.
- At the 12-month horizon, PCA + VAR(1) provides the most competitive forecast among the evaluated approaches.
- The evidence is exploratory and should be interpreted alongside the limitations of the missing-data treatment.

## Repository structure

- `notebooks/analisis_curva_banxico.ipynb` — primary notebook with analysis outputs
- `data/raw/banxico_auction_rates_monthly.csv` — raw input data (add locally if not already present)
- `_run_ffill_comparison.py` — compares the forward-fill treatments and summary metrics
- `_generate_brief_pdf.py` — generates the executive brief PDF
- `_refresh_main_notebook_outputs.py` — refreshes cached notebook outputs
- `_restore_levels_changes_explanation.py` — updates notebook explanatory text
- `docs/` — generated outputs, infographic, and HTML viewer
- `outputs/figures/` — charts and figures used in the brief and documentation

## HTML showcase

Open the project gallery here:

https://htmlpreview.github.io/?https://github.com/maxsantana-data2strategy/forecasting-mexican-yield-curve/blob/main/docs/index.html

## Notes

This project is intended as a clean, story-driven data-science portfolio repository. It follows a standard workflow: data preparation, dimensionality reduction, forecasting, validation, and business interpretation.

The raw dataset is expected to be placed under `data/raw/` before running the notebook or scripts. The project documentation and working scripts are included here to make the workflow reproducible and easy to review.

## License

MIT

## Tags

- data-science
- time-series
- forecasting
- PCA
- economics
- Mexico
