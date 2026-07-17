# PyAutoCTI Workspace — Agent Instructions

This is the tutorial and example workspace for **PyAutoCTI**, a Python library for calibrating and
modelling Charge Transfer Inefficiency (CTI) in CCD imaging. These are the canonical,
agent-agnostic instructions for this repo.

## Repository Structure

- `scripts/` — Runnable Python scripts, organised by topic:
  - `overview/` — the six-part introduction to CTI and CTI calibration
  - `dataset_1d/` — 1D CTI calibration datasets: simulators, modeling, correction, results,
    advanced (database, temporal)
  - `imaging_ci/` — 2D charge injection imaging: simulators, modeling, correction,
    data_preparation, results, advanced (chaining pipelines)
  - `plot/` — the plotting API guides (function-based `autocti.plot` API)
- `notebooks/` — Jupyter notebook versions, generated from `scripts/` (do not edit directly)
- `config/` — PyAutoCTI configuration YAML files
- `dataset/` — Example 1D and charge injection datasets (simulators regenerate them)
- `output/` — Model-fit results (generated at runtime, not committed)

## Running Scripts

Scripts are run **from the repository root** so relative paths to `dataset/` and `output/`
resolve correctly:

```bash
python scripts/dataset_1d/modeling/start_here.py
```

Each topic folder has a `start_here.py` that is the canonical, always-current reference for that
topic. Results/database examples depend on outputs produced by their section's modeling scripts.

### Standard imports

```python
import autofit as af
import autocti as ac
import autocti.plot as aplt
```

### arcticpy

`import autocti` requires **arcticpy** (the C++ arctic clocking code). It is not a pip
dependency of `autocti` — install it after numpy with:

```bash
pip install arcticpy==2.6 --no-build-isolation --no-deps
```

(It needs `libgsl-dev` and a C++ toolchain to build; see `PyAutoCTI/AGENTS.md` for the no-root
header workaround, and note a naive `pip install arcticpy` downgrades numpy below 2.0.)

## Testing / validation

Fast structural validation of scripts that run a non-linear search uses the test-mode knob:

```bash
PYAUTO_TEST_MODE=2 python scripts/dataset_1d/modeling/start_here.py
```

(`2` bypasses sampling entirely; `1` runs a reduced-iteration search; the variable is
`PYAUTO_TEST_MODE`, not `PYAUTOFIT_TEST_MODE`.)

Known test-mode artifact: bypass levels (2/3) evaluate the model at prior medians, so scripts
whose models assert an ordering between identically-prior'd parameters (e.g.
`trap_0.release_timescale < trap_1.release_timescale`) raise a `FitException` at the tied
medians. Real (non-bypass) runs resample such points gracefully — this is not a script bug.

In a sandboxed / restricted environment, point caches at writable directories:

```bash
NUMBA_CACHE_DIR=/tmp/numba_cache MPLCONFIGDIR=/tmp/matplotlib python scripts/...
```

## Notebooks vs Scripts

Notebooks in `notebooks/` are **generated** from the `.py` files in `scripts/`. **Always edit the
`.py` scripts, never the `.ipynb` notebooks directly.** Notebook regeneration runs through the
PyAutoBuild pipeline at release time.

## Multi-dataset fits

CTI calibration fits many datasets (e.g. injection normalizations) simultaneously. Analysis
summing (`analysis_1 + analysis_2`) was removed from PyAutoFit — multi-dataset fits wrap each
analysis in an `af.AnalysisFactor` sharing the model and combine them in an
`af.FactorGraphModel`:

```python
analysis_factor_list = [
    af.AnalysisFactor(prior_model=model, analysis=analysis) for analysis in analysis_list
]
factor_graph = af.FactorGraphModel(*analysis_factor_list)
result_list = search.fit(model=factor_graph.global_prior_model, analysis=factor_graph)
```

## Related Repos

The PyAutoCTI stack (all on the `PyAutoLabs` GitHub org):

- https://github.com/PyAutoLabs/PyAutoConf — configuration handling
- https://github.com/PyAutoLabs/PyAutoArray — arrays, layouts, regions, masks
- https://github.com/PyAutoLabs/PyAutoFit — model composition + non-linear search
- https://github.com/PyAutoLabs/PyAutoCTI — CTI clocking (arctic), datasets, fits, analyses
- https://github.com/PyAutoLabs/autocti_workspace_test — regression scripts + Euclid heritage
- https://github.com/PyAutoLabs/PyAutoBuild — notebook generation + CI

For local development these are typically cloned as siblings of this repo (`../PyAutoCTI`, etc.).

## Never rewrite history

Never rewrite pushed history on any repo with a remote — no `git init` over a
tracked repo, no force-push to `main`, no fresh-start "Initial commit", no
`filter-repo` / `filter-branch` / `rebase -i` on pushed branches. To get a
clean tree: `git fetch origin && git reset --hard origin/main && git clean -fd`.
