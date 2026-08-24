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
dependency of `autocti` — it is a source-only C++ sdist, and a naive `pip install arcticpy`
downgrades numpy below 2.0. Install it with:

```bash
sudo apt-get update && sudo apt-get install -y libgsl-dev
pip install --upgrade pip setuptools wheel   # BUILD deps — --no-build-isolation
pip install numpy cython                     #   will not supply these
pip install scipy matplotlib                 # RUNTIME deps --no-deps suppresses
pip install arcticpy==2.6 --no-build-isolation --no-deps
```

Both flags have to be paid back by hand, which is where installs go wrong:
`--no-build-isolation` means pip does not read arcticpy's `build-system.requires`, so build
deps must already be present (without `setuptools` the build fails with `BackendUnavailable:
Cannot import 'setuptools.build_meta'`, and Python 3.12+ venvs no longer ship it);
`--no-deps` means `arcticpy/__init__.py`'s import of `read_noise` — which imports `scipy` and
`matplotlib` — has nothing to import, so a successful build still fails at `import arcticpy`.

Verify with `python -c "import arcticpy; from importlib.metadata import version;
print(version('arcticpy'))"`. Note arcticpy exposes **no** `__version__` attribute, so
`arcticpy.__version__` raises `AttributeError` even on a healthy install.

The full note — including the no-root header workaround — is `PyAutoCTI/AGENTS.md`
§arcticpy. The recipe's single owner, and the single `arcticpy==2.6` pin, is
`PyAutoHeart/.github/actions/install-arcticpy`, the action every CTI repo's CI runs.

## Testing / validation

Fast structural validation of scripts that run a non-linear search uses the test-mode knob:

```bash
PYAUTO_TEST_MODE=2 python scripts/dataset_1d/modeling/start_here.py
```

(`2` bypasses sampling entirely; `1` runs a reduced-iteration search; the variable is
`PYAUTO_TEST_MODE`, not `PYAUTOFIT_TEST_MODE`.)

### Smoke tests (CI)

`smoke_tests.txt` is the curated allowlist run by CI on every PR, through
PyAutoHeart's reusable smoke workflow (thin caller in
`.github/workflows/smoke_tests.yml`, chain
`PyAutoNerves PyAutoFit PyAutoArray PyAutoCTI`). Run it locally with:

```bash
python .github/scripts/run_smoke.py
```

Per-script environment comes from `config/build/profile_smoke.yaml`
(`PYAUTO_TEST_MODE=2` by default). arcticpy is **not** installed by this repo's
epilogue — the caller passes `arcticpy: true` and Heart runs its own
`install-arcticpy` action first, so the recipe has one owner across every CTI
repo.

**Keep the list a small curated subset — do not mass-promote scripts.** The
`modeling/start_here.py`-class scripts became smokeable only once PyAutoFit#1520
(`438f56fac`) made the `PYAUTO_TEST_MODE=2/3` bypass pick a deterministic
assertion-valid point: before it, ordered trap models with identical priors tied
at the prior medians and the bypass hard-failed. All nine now run bypassed, but
they are not all cheap. Measured 2026-08-24 (Python 3.12, PyAutoFit at
`438f56fac`):

| script | time | promoted |
|---|---|---|
| `dataset_1d/modeling/start_here.py` | 13 s | yes |
| `dataset_1d/modeling/customize/priors.py` | 12 s | no |
| `dataset_1d/modeling/features/species_x3.py` | 18 s | yes |
| `dataset_1d/modeling/features/visualize_full.py` | 20 s | no |
| `imaging_ci/modeling/start_here.py` | 96 s | yes |
| `imaging_ci/modeling/features/cosmic_rays.py` | 120 s | no |
| `imaging_ci/modeling/features/non_uniform.py` | 53 s | no |
| `imaging_ci/modeling/features/serial_cti.py` | 94 s | no |
| `imaging_ci/modeling/features/visualize_full.py` | 96 s | no |

All nine pass. The three promoted cover both dataset geometries and the
multi-species ordered-trap case — the surface the bypass fix unblocked — and run
in **132 s** measured cold, i.e. with `dataset/` wiped to its committed state so
every dataset is simulated first, which is what CI does on a fresh checkout. The
full set of nine would cost ~522 s. Promote further scripts deliberately, with a
timing, rather than in bulk.

(Per-script times above are each script's own cold cost. They do not sum to the
suite total: consecutive scripts sharing a dataset only simulate it once.)

In a sandboxed / restricted environment, point caches at writable directories:

```bash
NUMBA_CACHE_DIR=/tmp/numba_cache MPLCONFIGDIR=/tmp/matplotlib python scripts/...
```

### Navigator catalogue (CI)

`llms-full.txt` and `workspace_index.json` in the repo root are the **generated**
LLM-facing catalogue of every script in `scripts/`. They are checked by the
`Navigator Check` workflow (`.github/workflows/navigator_check.yml`, a thin
caller of PyAutoHands' reusable `navigator_check.yml`), which runs three jobs:
a path/banner lint, an unbatched multi-start search guard, and a **staleness**
job that regenerates the catalogue and fails if it drifts from `scripts/`.

Regenerate after adding, renaming, moving or re-titling any script, and commit
the result alongside the script change:

```bash
git clone https://github.com/PyAutoLabs/PyAutoHands.git ../PyAutoHands
python3 ../PyAutoHands/autohands/regenerate_navigator.py autocti
```

Run it from the workspace root — the generator catalogues the current working
directory. It needs only `pyyaml`, not the science stack, and its output is
deterministic (two runs are byte-identical).

Two things to know before editing a script header:

- The catalogue's per-script summary is the **first prose paragraph** of the
  opening docstring, and the title line is only recognised as a title when the
  line beneath it is a `=` underline. A `-----` underline is not recognised, so
  the dashes become the summary — which is what 12 scripts did before
  autocti_workspace#29. Use `=`.
- 13 scripts still have no prose paragraph at all and catalogue as
  `(no summary in script docstring)`. That is a documentation gap, not a CI
  failure; the check does not gate on it.

**Notebook regeneration is a separate thing and is currently blocked for this
workspace:** `autohands/generate.py` rejects any project absent from
`build_util.COLAB_PROJECTS`, and `autocti` is not registered there (nor in
PyAutoNerves' `setup_colab.py`). `regenerate_navigator.py` is unaffected — it
never touches that registry.

## Notebooks vs Scripts

Notebooks in `notebooks/` are **generated** from the `.py` files in `scripts/`. **Always edit the
`.py` scripts, never the `.ipynb` notebooks directly.** Notebook regeneration runs through the
PyAutoHands pipeline at release time.

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

- https://github.com/PyAutoLabs/PyAutoNerves — configuration handling
- https://github.com/PyAutoLabs/PyAutoArray — arrays, layouts, regions, masks
- https://github.com/PyAutoLabs/PyAutoFit — model composition + non-linear search
- https://github.com/PyAutoLabs/PyAutoCTI — CTI clocking (arctic), datasets, fits, analyses
- https://github.com/PyAutoLabs/autocti_workspace_test — regression scripts + Euclid heritage
- https://github.com/PyAutoLabs/PyAutoHands — notebook generation + CI

For local development these are typically cloned as siblings of this repo (`../PyAutoCTI`, etc.).

## Never rewrite history

Never rewrite pushed history on any repo with a remote — no `git init` over a
tracked repo, no force-push to `main`, no fresh-start "Initial commit", no
`filter-repo` / `filter-branch` / `rebase -i` on pushed branches. To get a
clean tree: `git fetch origin && git reset --hard origin/main && git clean -fd`.
