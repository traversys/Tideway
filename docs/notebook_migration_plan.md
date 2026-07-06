# Notebook Migration Plan

## Goal

Move notebooks from Dismal-era assumptions to Tideway's public architecture. Notebooks should demonstrate Tideway usage and delegate report behavior to Tideway APIs instead of duplicating Dismal internals, parsing Dismal XML files, or importing `core`.

## Checklist

- [x] Save this plan in the repository.
- [x] Add shared notebook helpers for config loading, appliance creation, output paths, and result-to-DataFrame conversion.
- [x] Add a notebook audit script that detects Dismal-era architecture patterns.
- [x] Convert straightforward health/admin/deep-dive report notebooks to `tw.reports()` or `tw.report_admin()`.
- [x] Isolate remaining custom-analysis notebooks in the audit allowlist.
- [ ] Convert remaining custom-analysis notebooks so they use public Tideway APIs only.
- [x] Run `python3 scripts/check_notebooks.py`.
- [x] Run `PYTHONPYCACHEPREFIX=/private/tmp/tideway-pyc python3 -m compileall tideway`.
- [x] Run `python3 -m pytest`.

## Progress Notes

- Added `tideway.notebooks` for shared notebook setup and result conversion.
- Added `scripts/check_notebooks.py` to prevent reintroducing `core`, `dismal_queries.xml`, or direct Discovery `requests.Session` usage in standard notebooks.
- Converted straightforward report notebooks to `tw.reports()` and admin mutation examples to `tw.report_admin()`.
- Left `notebooks/health/device_analysis.ipynb` and `notebooks/deep_dive/app_model_explore.ipynb` on the audit allowlist for a later custom-analysis pass because they are not simple one-report notebooks.

## Migration Rules

- Use `tideway.notebooks.appliance_from_config(...)` for config/token setup.
- Use `tw.reports().<report_name>(...)` for Dismal report equivalents.
- Use `tw.report_admin()` for admin operations such as schedule timezone updates.
- Use `tideway.notebooks.report_to_dataframe(result)` for display-friendly tables.
- Keep notebook-specific dependencies only when the notebook genuinely needs them, such as `itables`, `matplotlib`, or `numpy`.
- Do not import `core`, parse `dismal_queries.xml`, or create `requests.Session` for Discovery API calls in standard report notebooks.

## Stages

### Stage 1: Foundation

Add `tideway/notebooks.py` and `scripts/check_notebooks.py`. The helper module centralizes repeated setup currently copied across notebooks. The audit script gives a fast guardrail for future notebook additions.

### Stage 2: Straightforward Report Notebooks

Replace report notebooks whose primary purpose is to generate one Dismal report with calls to `tw.reports()`. These notebooks should become short examples that load config, run the report, display the DataFrame, and optionally write canonical output files.

### Stage 3: Admin And Lookup Notebooks

Move admin workflows to `tw.report_admin()` and lookup workflows to public report/data APIs. Add missing public parameters where a notebook exposes report-specific input such as an IP address.

### Stage 4: Custom Analysis

Review notebooks that do more than one report, such as device analysis, app model exploration, and KPI licensing. Keep the analysis logic, but replace internal Dismal dependencies and direct REST plumbing with public Tideway APIs.
