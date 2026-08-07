# Simulate every workspace dataset. All datasets are ignored by git and are
# regenerated at runtime by the example scripts' `__Dataset Auto-Simulation__`
# guards; run this script to (re)build them all up front instead. The only
# committed files under `dataset/` are the five hand-made overview media
# illustrations, which no simulator writes.
python scripts/dataset_1d/simulators/start_here.py
python scripts/dataset_1d/simulators/examples/overview.py
python scripts/dataset_1d/simulators/examples/species_x1_continuum.py
python scripts/dataset_1d/simulators/examples/species_x3.py
python scripts/dataset_1d/simulators/examples/temporal.py

python scripts/imaging_ci/simulators/start_here.py
python scripts/imaging_ci/simulators/examples/bias_uncorrected.py
python scripts/imaging_ci/simulators/examples/cosmic_rays.py
python scripts/imaging_ci/simulators/examples/non_uniform.py
python scripts/imaging_ci/simulators/examples/parallel_and_serial.py
python scripts/imaging_ci/simulators/examples/poisson_traps.py
python scripts/imaging_ci/simulators/examples/serial_cti.py

python scripts/imaging_ci/simulators/overview/calibrate.py
python scripts/imaging_ci/simulators/overview/non_uniform_cosmic_rays.py
python scripts/imaging_ci/simulators/overview/uniform.py
